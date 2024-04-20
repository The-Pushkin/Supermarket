from flask import Flask, request, jsonify, make_response
from peewee import PostgresqlDatabase, Model, IntegerField, CharField, FloatField, AutoField
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Harambe_is_love_Harambe_is_life'

db = PostgresqlDatabase(
    'supermarket',  # Database name
    user='student',
    password='student',
    host='localhost',
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

# Creates the DB connection and tables.
def initialize_db():
    db.connect()
    db.create_tables([Product, User], safe=True)
    insert_user_safe("admin", generate_password_hash("admin"), "admin")

# Inserts a new product into the database.
def insert_product(name, price, stock):
    try:
        product = Product.create(product_name=name, product_price=price, product_stock=stock)
        return product
    except Exception as e:
        print(f"[ERROR] Insert error: {e}")
        return e
    
# Inserts a new user into the database.
def insert_user(name, password, role):
    try:
        user = User.create(user_name=name, user_password=password, user_role=role)
        return user
    except Exception as e:
        print(f"[ERROR] Insert error: {e}")
        return e
    
# insert_user that doesn't produce errors on conflict
def insert_user_safe(name, password, role):
    try:
        user = User.get(User.user_name == name)
        return user
    except Exception as e:
        user = User.insert(user_name=name, user_password=password, user_role=role).on_conflict_ignore().execute()

# Updates the stock of a product by a specific increment.
def update_product_stock(product_name, increment):
    try:
        product = Product.get(Product.product_name == product_name)
        query = Product.update(product_stock=Product.product_stock + increment).where(Product.product_name == product_name)
        query.execute()
        return None
    except Exception as e:
        print(f"[ERROR] Update error: {e}")
        return e

# Returns a product by its name.
def select_product(product_name):
    try:
        product = Product.get(Product.product_name == product_name)
        return product
    except Exception as e:
        print(f"[ERROR] Select error: {e}")
        return e
    
# Returns a user by its name.
def select_user(user_name):
    try:
        user = User.get(User.user_name == user_name)
        return user
    except Exception as e:
        print(f"[ERROR] Select error: {e}")
        return e

# Returns a list of all products in the DB.
def select_products():
    products = Product.select()
    return list(products)

# Returns a list of all users in the DB.
def select_users():
    users = User.select()
    return list(users)

@app.route('/add-product', methods=['POST'])
def route_add_product():
    data = request.json
    
    if not data or 'product_name' not in data or 'product_price' not in data or 'product_stock' not in data:
        return jsonify({'error': 'Missing product details'}), 400

    product = insert_product(data['product_name'], data['product_price'], data['product_stock'])
    if isinstance(product, Exception):
        return jsonify({'error': str(product)}), 500
    
    return jsonify({
        'message': 'Product added successfully',
        'product_id': product.product_id
    }), 201

@app.route('/add-user', methods=['POST'])
def route_add_user():
    data = request.json
    
    if not data or 'user_name' not in data or 'user_password' not in data or 'user_role' not in data:
        return jsonify({'error': 'Missing user details'}), 400

    user = insert_user(data['user_name'], data['user_password'], data['user_role'])
    if isinstance(user, Exception):
        return jsonify({'error': str(user)}), 500
    
    return jsonify({
        'message': 'User added successfully',
        'user_id': user.user_id
    }), 201

@app.route('/update-stock', methods=['PUT'])
def route_update_stock():
    data = request.json
    
    if not data or 'product_name' not in data or 'increment' not in data:
        return jsonify({'error': 'Missing product details'}), 400

    result = update_product_stock(data['product_name'], data['increment'])
    if isinstance(result, Exception):
        return jsonify({'error': str(result)}), 500
    
    return jsonify({
        'message': 'Stock updated successfully'
    }), 201

@app.route('/get-product', methods=['GET'])
def route_get_product():
    data = request.json
    
    if not data or 'product_name' not in data:
        return jsonify({'error': 'Missing product name'}), 400

    product = select_product(data['product_name'])
    if isinstance(product, Exception):
        return jsonify({'error': str(product)}), 500
    
    return jsonify({
        "product_id": product.product_id,
        "product_name": product.product_name,
        "product_price": product.product_price,
        "product_stock": product.product_stock
    }), 201

@app.route('/get-user', methods=['GET'])
def route_get_user():
    data = request.json
    
    if not data or 'user_name' not in data:
        return jsonify({'error': 'Missing user name'}), 400

    user = select_user(data['user_name'])
    if isinstance(user, Exception):
        return jsonify({'error': str(user)}), 500
    
    return jsonify({
        "user_id": user.user_id,
        "user_name": user.user_name,
        "user_password": user.user_password,
        "user_role": user.user_role
    }), 201

@app.route('/all-products', methods=['GET'])
def route_all_products():
    products = select_products()
    
    return jsonify({
        "products": [
            {"product_id": product.product_id,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "product_stock": product.product_stock}
            for product in products
        ]
    }), 201

@app.route('/all-users', methods=['GET'])
def route_all_users():
    users = select_users()
    
    return jsonify({
        "users": [
            {"user_id": user.user_id,
            "user_name": user.user_name,
            "user_password": user.user_password,
            "user_role": user.user_role}
            for user in users
        ]
    }), 201

if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)