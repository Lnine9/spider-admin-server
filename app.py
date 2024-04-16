import logging
import os

from flask import request, make_response, Response
from flask_cors import CORS
from router import register_blueprint
from utils.JWT_token import decode_jwt_token, generate_jwt_token
from utils.flask_ext.flask_app import FlaskApp

app = FlaskApp(__name__)
CORS(app)

register_blueprint(app)


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        return make_response()

    '''将jwt生成的私钥放入环境变量中'''
    if os.getenv('JWT_SECRET_KEY') is None:
        try:
            with open('./secretkey.txt', 'r') as file:
                secret_key = file.read()
                os.environ['JWT_SECRET_KEY'] = secret_key
        except FileNotFoundError as e:
            logging.error(e)

    '''设置页面登录拦截，判断token是否存在或过期'''
    if (request.path.startswith('/api/sign') or request.path.startswith('/api/spider')) is False:
        token = request.headers.get('Authorization')
        if token is None:
            return Response('用户未登录', 401)
        auth = decode_jwt_token(token)
        if auth is None:
            return Response('token已过期', 401)


@app.after_request
def after_request(response):
    '''刷新token'''
    if (request.path.startswith('/api/sign') or request.path.startswith('/api/spider')) is False:
        token = request.headers.get('Authorization')
        if token is not None:
            auth = decode_jwt_token(token)
            refresh_token = generate_jwt_token(auth)
            response.headers['Authorization'] = refresh_token
    return response


if __name__ == '__main__':
    app.run(port=2024, debug=True)
