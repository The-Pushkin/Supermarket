from flask import Flask, request, jsonify, make_response
import requests

port = 5000

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Harambe_is_love_Harambe_is_life'

db_api_url = 'http://localhost:5010/'
headers={
    'Content-type':'application/json', 
    'Accept':'application/json'
}

# Adds a new product to the database.
@app.route('/add-product', methods=['POST'])
def route_add_product():
    data = request.json
    
    if not data or 'product_name' not in data or 'product_price' not in data or 'product_stock' not in data:
        return jsonify({'error': 'Missing product details'}), 400

    response = requests.post(db_api_url + 'insert-product', headers=headers, json=data)
    response_json = response.json()
    
    if response_json['message'] == "insert_success":
        return jsonify({
            'message': 'Product added successfully',
            'product_id': response_json['product_id']
        }), 201
    else:
        return jsonify({'error': response_json['error']}), 500

# Adds a new user to the database.
@app.route('/add-user', methods=['POST'])
def route_add_user():
    data = request.json
    
    if not data or 'user_name' not in data or 'user_password' not in data or 'user_role' not in data:
        return jsonify({'error': 'Missing user details'}), 400

    response = requests.post(db_api_url + 'insert-user', headers=headers, json=data)
    response_json = response.json()
    
    if response_json['message'] == "insert_success":
        return jsonify({
            'message': 'User added successfully',
            'user_id': response_json['user_id']
        }), 201
    else:
        return jsonify({'error': response_json['error']}), 500

@app.route('/update-stock', methods=['PUT'])
def route_update_stock():
    data = request.json
    
    if not data or 'product_name' not in data or 'increment' not in data:
        return jsonify({'error': 'Missing product details'}), 400

    response = requests.get(db_api_url + 'select-product', headers=headers, json=data)
    response_json = response.json()
    
    if response_json['message'] != "select_success":
        return jsonify({'error': 'Product not found'}), 500
    
    new_stock = response_json['product_stock'] + data['increment']
    
    response = requests.put(db_api_url + 'update-product-stock', headers=headers, json={
        'product_name': data['product_name'],
        'new_stock': new_stock
    })
    response_json = response.json()
    
    if response_json['message'] == "update_success":
        return jsonify({
            'message': 'Stock updated successfully'
        }), 201
    else:
        return jsonify({'error': response_json['error']}), 500

@app.route('/get-product', methods=['GET'])
def route_get_product():
    data = request.json
    
    if not data or 'product_name' not in data:
        return jsonify({'error': 'Missing product name'}), 400

    response = requests.get(db_api_url + 'select-product', headers=headers, json=data)
    response_json = response.json()
    
    if response_json['message'] != "select_success":
        return jsonify({'error': 'Product not found'}), 500
    else:
        return jsonify({
            "product_id": response_json['product_id'],
            "product_name": data['product_name'],
            "product_price": response_json['product_price'],
            "product_stock": response_json['product_stock']
        }), 201

@app.route('/get-user', methods=['GET'])
def route_get_user():
    data = request.json
    
    if not data or 'user_name' not in data:
        return jsonify({'error': 'Missing user name'}), 400

    response = requests.get(db_api_url + 'select-user', headers=headers, json=data)
    response_json = response.json()
    
    if response_json['message'] != "select_success":
        return jsonify({'error': 'User not found'}), 500
    else:
        return jsonify({
            "user_id": response_json['user_id'],
            "user_name": data['user_name'],
            "user_password": response_json['user_password'],
            "user_role": response_json['user_role']
        }), 201

@app.route('/all-products', methods=['GET'])
def route_all_products():
    response = requests.get(db_api_url + 'select-products', headers=headers)
    response_json = response.json()
    
    return jsonify({
        "products": response_json['products']
    }), 201

@app.route('/all-users', methods=['GET'])
def route_all_users():
    response = requests.get(db_api_url + 'select-users', headers=headers)
    response_json = response.json()
    
    return jsonify({
        "users": response_json['users']
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=port)