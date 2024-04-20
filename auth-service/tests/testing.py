import requests

url = "http://127.0.0.1:5005/login"

def test_auth(auth, test_name):
    try:
        response = requests.post(url, data={}, auth=auth)
        print(f"{test_name} response:\n{response.text}\n")
    except requests.exceptions.RequestException as e:
        print(f"{test_name} exception:\n{e}\n")

test_auth(("admin", "admin"), "test_login_success")
test_auth(("admin", "wrong_password"), "test_login_admin_fail_wrong password")
test_auth(("wrong_username", "admin"), "test_login_user_fail_wrong_username")
