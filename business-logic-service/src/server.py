from peewee import PostgresqlDatabase, Model, IntegerField, CharField, FloatField, AutoField

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

# Inserts a new product into the database.
def insert_product(name, price, stock):
    try:
        product = Product.create(product_name=name, product_price=price, product_stock=stock)
        return product
    except Exception as e:
        print(f"Insert error: {e}")
        return None
    
# Inserts a new user into the database.
def insert_user(name, password, role):
    try:
        user = User.create(user_name=name, user_password=password, user_role=role)
        return user
    except Exception as e:
        print(f"Insert error: {e}")
        return None

# Updates the stock of a product by a specific increment.
def update_product_stock(product_id, increment):
    try:
        product = Product.get(Product.product_id == product_id)
        query = Product.update(product_stock=Product.product_stock + increment).where(Product.product_id == product_id)
        query.execute()
    except Exception as e:
        print(f"Update error: {e}")
        return

# Returns a product by its ID.
def select_product(product_id):
    try:
        product = Product.get(Product.product_id == product_id)
        return product
    except Exception as e:
        print(f"Select error: {e}")
        return None
    
# Returns a user by its ID.
def select_user(user_id):
    try:
        user = User.get(User.user_id == user_id)
        return user
    except Exception as e:
        print(f"Select error: {e}")
        return None

# Returns a list of all products in the DB.
def select_products():
    products = Product.select()
    return list(products)

# Returns a list of all users in the DB.
def select_users():
    users = User.select()
    return list(users)

# TODO: Make this file into a Flask server and move testing to a separate file.
def test_db():
    new_product = insert_product("Cheese", 3.99, 50)
    if not new_product:
        print("Failed to add product.")
        return
    print(f"Added product: {new_product.product_name}")
    
    new_user = insert_user("the_admin", "admin123", "admin")
    if not new_user:
        print("Failed to add user.")
        return
    print(f"Added user: {new_user.user_name}")

    update_product_stock(new_product.product_id, 45)
    print("Updated product stock.")

    product = select_product(new_product.product_id)
    if product:
        print(f"Product ID {product.product_id}: {product.product_name} - Stock: {product.product_stock}")
    
    user = select_user(new_user.user_id)
    if user:
        print(f"User ID {user.user_id}: {user.user_name} - Role: {user.user_role}")

    print("All Products:")
    for product in select_products():
        print(f"{product.product_id}: {product.product_name} - {product.product_stock}")
        
    print("All Users:")
    for user in select_users():
        print(f"{user.user_id}: {user.user_name} - {user.user_role}")

if __name__ == '__main__':
    initialize_db()
    test_db()