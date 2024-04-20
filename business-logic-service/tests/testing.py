import requests

def test_request(path, test_name, json, request_type):
    url = "http://127.0.0.1:5000" + path
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

# add-product
test_request(
    "/add-product",
    "test_add_product_success",
    {
        "product_name": "Castravete Fabio",
        "product_price": 3.99,
        "product_stock": 50
    },
    "POST"
)
test_request(
    "/add-product",
    "test_add_product_fail_already_exists",
    {
        "product_name": "Castravete Fabio",
        "product_price": 12.2,
        "product_stock": 123
    },
    "POST"
)
test_request(
    "/add-product",
    "test_add_product_fail_missing_name",
    {
        "product_price": 1.99,
        "product_stock": 100
    },
    "POST"
)
test_request(
    "/add-product",
    "test_add_product_fail_missing_price",
    {
        "product_name": "Mere Golden",
        "product_stock": 100
    },
    "POST"
)
test_request(
    "/add-product",
    "test_add_product_fail_missing_stock",
    {
        "product_name": "Mere Florina",
        "product_price": 1.99
    },
    "POST"
)

# add-user
test_request(
    "/add-user",
    "test_add_user_success",
    {
        "user_name": "user",
        "user_password": 3.99,
        "user_role": "cashier"
    },
    "POST"
)
test_request(
    "/add-user",
    "test_add_user_fail_already_exists",
    {
        "user_name": "user",
        "user_password": 12.2,
        "user_role": "restock"
    },
    "POST"
)
test_request(
    "/add-user",
    "test_add_user_fail_missing_name",
    {
        "user_password": 1.99,
        "user_role": "restock"
    },
    "POST"
)
test_request(
    "/add-user",
    "test_add_user_fail_missing_password",
    {
        "user_name": "ana",
        "user_role": "restock"
    },
    "POST"
)
test_request(
    "/add-user",
    "test_add_user_fail_missing_role",
    {
        "user_name": "oana",
        "user_password": 1.99
    },
    "POST"
)

# update-stock
test_request(
    "/update-stock",
    "test_update_stock_success",
    {
        "product_name": "Castravete Fabio",
        "increment": 10
    },
    "PUT"
)
test_request(
    "/update-stock",
    "test_update_stock_fail_not_found",
    {
        "product_name": "Branza de capra",
        "increment": 10
    },
    "PUT"
)
test_request(
    "/update-stock",
    "test_update_stock_fail_missing_name",
    {
        "increment": 10
    },
    "PUT"
)
test_request(
    "/update-stock",
    "test_update_stock_fail_missing_increment",
    {
        "product_name": "Mere Golden"
    },
    "PUT"
)

# get-product
test_request(
    "/get-product",
    "test_get_product_success",
    {
        "product_name": "Castravete Fabio"
    },
    "GET"
)
test_request(
    "/get-product",
    "test_get_product_fail_not_found",
    {
        "product_name": "Branza de capra"
    },
    "GET"
)
test_request(
    "/get-product",
    "test_get_product_fail_missing_name",
    {},
    "GET"
)

# get-user
test_request(
    "/get-user",
    "test_get_user_success",
    {
        "user_name": "user"
    },
    "GET"
)
test_request(
    "/get-user",
    "test_get_user_fail_not_found",
    {
        "user_name": "ioana"
    },
    "GET"
)
test_request(
    "/get-user",
    "test_get_user_fail_missing_name",
    {},
    "GET"
)

# all-products
test_request(
    "/all-products",
    "test_all_products",
    {},
    "GET"
)

# all-users
test_request(
    "/all-users",
    "test_all_users",
    {},
    "GET"
)
