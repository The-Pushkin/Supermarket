import jwt
import datetime
import requests
from flask import Flask, request, jsonify, make_response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from loki_logger import LokiLogger


port = 5005

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tH15_1s_Wh4T_Th3_3Dg3_0f_Y0uR_534T_W4s_mAd3_0f'

jwt_token_timeout = 30  # minutes

logger = LokiLogger(service_name="auth-service").get_logger()

def get_user(username):
    url = "http://bussines_logic_service:5000/get-user"
    json = {"user_name": username}
    headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
    }
    
    response = requests.get(url, headers=headers, data={}, json=json)
    if response.status_code != 201:
        logger.error(f"[ERROR] (Status code: {response.status_code})\nResponse: {response.text}\n")
        return None
    return response.json()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = get_user(data['username'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login_user():
    logger.info("[INFO] login call")
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Missing auth data\n', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = get_user(auth.username)

    if not user:
        return make_response('User does not exist\n', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user['user_password'], auth.password):
        token = jwt.encode({'username': user['user_name'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=jwt_token_timeout)}, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return make_response('Wrong password for the username\n', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

if __name__ == '__main__':
    app.run(debug=True, port=port)
