from flask import Flask, request, jsonify, make_response
from peewee import PostgresqlDatabase, Model, IntegerField, CharField, FloatField, AutoField
from werkzeug.security import generate_password_hash
from loki_logger import LokiLogger

port = 5010

app = Flask(__name__)

app.config['SECRET_KEY'] = 'B0B3R_CRwa'

logger = LokiLogger(service_name="database-api-service").get_logger()

db = PostgresqlDatabase(
    'supermarket',  # Database name
    user='student',
    password='student',
    host='postgresql',
    port=5432
)

# Product model.
class Product(Model):
    product_id = AutoField(primary_key=True)
    product_name = CharField()
    product_price = FloatField()
    product_stock = IntegerField()
    class Meta:
        database = db
        table_name = 'products'
        
# User model.
class User(Model):
    user_id = AutoField(primary_key=True)
    user_name = CharField()
    user_password = CharField()
    user_role = CharField()
    class Meta:
        database = db
        table_name = 'users'

# insert_user that doesn't produce errors on conflict
def insert_user_safe(name, password, role):
    try:
        user = User.get(User.user_name == name)
        return user
    except Exception as e:
        user = User.insert(user_name=name, user_password=password, user_role=role).on_conflict_ignore().execute()

# Creates the DB connection and tables.
def initialize_db():
    db.connect()
    db.create_tables([Product, User], safe=True)
    insert_user_safe("admin", generate_password_hash("admin"), "admin")

# Inserts a new product into the database.
@app.route('/insert-product', methods=['POST'])
def insert_product():
    logger.info("[INFO] insert-product call")
    data = request.json
    
    try:
        product = Product.create(
            product_name=data['product_name'],
            product_price=data['product_price'],
            product_stock=data['product_stock']
        )
        
        return jsonify({
            'message': 'insert_success',
            'product_id': product.product_id
        }), 201
    except Exception as e:
        logger.error(f"[ERROR] Insert error: {e}")
        return jsonify({
            'message': 'insert_fail',
            'error': str(e)
        }), 500
    
# Inserts a new user into the database.
@app.route('/insert-user', methods=['POST'])
def insert_user():
    logger.info("[INFO] insert-user call")
    data = request.json
    
    try:
        user = User.create(
            user_name=data['user_name'],
            user_password=data['user_password'],
            user_role=data['user_role']
        )
        
        return jsonify({
            'message': 'insert_success',
            'user_id': user.user_id
        }), 201
    except Exception as e:
        logger.error(f"[ERROR] Insert error: {e}")
        return jsonify({
            'message': 'insert_fail',
            'error': str(e)
        }), 500

# Updates the stock of a product by a specific increment.
@app.route('/update-product-stock', methods=['PUT'])
def update_product_stock():
    logger.info("[INFO] update-product-stock call")
    data = request.json
    
    try:
        query = Product.update(product_stock=data['new_stock']).where(Product.product_name == data['product_name'])
        query.execute()
        
        return jsonify({
            'message': 'update_success'
        }), 201
    except Exception as e:
        logger.error(f"[ERROR] Update error: {e}")
        return jsonify({
            'message': 'update_fail',
            'error': str(e)
        }), 500

# Returns a product by its name.
@app.route('/select-product', methods=['GET'])
def select_product():
    logger.info("[INFO] select-product call")
    data = request.json
    
    try:
        product = Product.get(Product.product_name == data['product_name'])
        
        return jsonify({
            "message": "select_success",
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "product_stock": product.product_stock
        }), 201
    except Exception as e:
        logger.error(f"[ERROR] Select error: {e}")
        return jsonify({
            "message": "select_fail",
            "error": str(e)
        }), 500
    
# Returns a user by its name.
@app.route('/select-user', methods=['GET'])
def select_user():
    logger.info("[INFO] select-user call")
    data = request.json
    
    try:
        user = User.get(User.user_name == data['user_name'])
        
        return jsonify({
            "message": "select_success",
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_password": user.user_password,
            "user_role": user.user_role
        }), 201
    except Exception as e:
        logger.error(f"[ERROR] Select error: {e}")
        return jsonify({
            "message": "select_fail",
            "error": str(e)
        }), 500

# Returns a list of all products in the DB.
@app.route('/select-products', methods=['GET'])
def select_products():
    logger.info("[INFO] select-products call")
    products = list(Product.select())
    
    return jsonify({
        "products": [
            {"product_id": product.product_id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "product_stock": product.product_stock}
            for product in products
        ]
    }), 201

# Returns a list of all users in the DB.
@app.route('/select-users', methods=['GET'])
def select_users():
    logger.info("[INFO] select-users call")
    users = list(User.select())
    
    return jsonify({
        "users": [
            {"user_id": user.user_id,
            "user_name": user.user_name,
            "user_password": user.user_password,
            "user_role": user.user_role}
            for user in users
        ]
    }), 201
    
# Clears the database.
@app.route('/clear-db', methods=['POST'])
def clear_db():
    logger.info("[INFO] clear-db call")
    try:
        Product.delete().execute()
        User.delete().execute()
        
        return jsonify({
            'message': 'clear_success'
        }), 201
    except Exception as e:
        logger.error(f"[ERROR] Delete error: {e}")
        return jsonify({
            'message': 'clear_fail',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True, port=port)