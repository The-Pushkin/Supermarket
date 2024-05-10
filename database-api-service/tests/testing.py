import requests

def test_request(path, test_name, json, request_type):
    url = "http://127.0.0.1:5010" + path
    headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
    }
    
    try:
        if request_type == "POST":
            response = requests.post(url, headers=headers, data={}, json=json)
        elif request_type == "PUT":
            response = requests.put(url, headers=headers, data={}, json=json)
        else:
            response = requests.get(url, headers=headers, data={}, json=json)
        print(f"{test_name} response:\n{response.text}\n")
    except requests.exceptions.RequestException as e:
        print(f"{test_name} exception:\n{e}\n")

test_request(
    "/clear-db",
    "test_clear_db",
    {},
    "POST"
)

# insert-product
test_request(
    "/insert-product",
    "test_insert_product_success",
    {
        "product_name": "Castravete Fabio",
        "product_price": 3.99,
        "product_stock": 50
    },
    "POST"
)
test_request(
    "/insert-product",
    "test_insert_product_fail_already_exists",
    {
        "product_name": "Castravete Fabio",
        "product_price": 12.2,
        "product_stock": 123
    },
    "POST"
)
test_request(
    "/insert-product",
    "test_insert_product_fail_missing_name",
    {
        "product_price": 1.99,
        "product_stock": 100
    },
    "POST"
)
test_request(
    "/insert-product",
    "test_insert_product_fail_missing_price",
    {
        "product_name": "Mere Golden",
        "product_stock": 100
    },
    "POST"
)
test_request(
    "/insert-product",
    "test_insert_product_fail_missing_stock",
    {
        "product_name": "Mere Florina",
        "product_price": 1.99
    },
    "POST"
)

# insert-user
test_request(
    "/insert-user",
    "test_insert_user_success",
    {
        "user_name": "user",
        "user_password": 3.99,
        "user_role": "cashier"
    },
    "POST"
)
test_request(
    "/insert-user",
    "test_insert_user_fail_already_exists",
    {
        "user_name": "user",
        "user_password": 12.2,
        "user_role": "restock"
    },
    "POST"
)
test_request(
    "/insert-user",
    "test_insert_user_fail_missing_name",
    {
        "user_password": 1.99,
        "user_role": "restock"
    },
    "POST"
)
test_request(
    "/insert-user",
    "test_insert_user_fail_missing_password",
    {
        "user_name": "ana",
        "user_role": "restock"
    },
    "POST"
)
test_request(
    "/insert-user",
    "test_insert_user_fail_missing_role",
    {
        "user_name": "oana",
        "user_password": 1.99
    },
    "POST"
)

# update-product-stock
test_request(
    "/update-product-stock",
    "test_update_product_stock_success",
    {
        "product_name": "Castravete Fabio",
        "new_stock": 10
    },
    "PUT"
)
test_request(
    "/update-product-stock",
    "test_update_product_stock_fail_not_found",
    {
        "product_name": "Branza de capra",
        "new_stock": 10
    },
    "PUT"
)
test_request(
    "/update-product-stock",
    "test_update_product_stock_fail_missing_name",
    {
        "new_stock": 10
    },
    "PUT"
)
test_request(
    "/update-product-stock",
    "test_update_product_stock_fail_missing_new_stock",
    {
        "product_name": "Mere Golden"
    },
    "PUT"
)

# select-product
test_request(
    "/select-product",
    "test_select_product_success",
    {
        "product_name": "Castravete Fabio"
    },
    "select"
)
test_request(
    "/select-product",
    "test_select_product_fail_not_found",
    {
        "product_name": "Branza de capra"
    },
    "select"
)
test_request(
    "/select-product",
    "test_select_product_fail_missing_name",
    {},
    "select"
)

# select-user
test_request(
    "/select-user",
    "test_select_user_success",
    {
        "user_name": "user"
    },
    "select"
)
test_request(
    "/select-user",
    "test_select_user_fail_not_found",
    {
        "user_name": "ioana"
    },
    "select"
)
test_request(
    "/select-user",
    "test_select_user_fail_missing_name",
    {},
    "select"
)

# select-products
test_request(
    "/select-products",
    "test_select_products",
    {},
    "select"
)

# select-users
test_request(
    "/select-users",
    "test_select_users",
    {},
    "select"
)
