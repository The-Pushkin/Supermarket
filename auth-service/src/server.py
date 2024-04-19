from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tH15_1s_Wh4T_Th3_3Dg3_0f_Y0uR_534T_W4s_mAd3_0f'

jwt_token_timeout = 30  # minutes

# Dummy user store
users = [
    {
        "username": "admin",
        "password": generate_password_hash("admin123"),
        "role": "admin",
    },
    {
        "username": "uyuy",
        "password": generate_password_hash("uyuy"),
        "role": "user",
    },
]

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
            current_user = next((user for user in users if user['username'] == data['username']), None)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Missing auth data\n', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = next((user for user in users if user['username'] == auth.username), None)

    if not user:
        return make_response('User does not exist\n', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user['password'], auth.password):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=jwt_token_timeout)}, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return make_response('Wrong password for the username\n', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

if __name__ == '__main__':
    app.run(debug=True)
