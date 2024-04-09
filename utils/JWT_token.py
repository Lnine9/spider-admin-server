import jwt
import datetime
import os


def generate_jwt_token(data):
    secret_key = os.environ.get('JWT_SECRET_KEY')  # 从环境变量中获取密钥
    algorithm = 'HS256'
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    token_data = {
        'data': data,
        'exp': expires_at
    }

    token = jwt.encode(token_data, secret_key, algorithm=algorithm)
    return token


def decode_jwt_token(token):
    secret_key = os.environ.get('JWT_SECRET_KEY')  # 从环境变量中获取密钥
    algorithm = 'HS256'
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload.get('data')
    except jwt.ExpiredSignatureError:
        # Token已过期
        return None
    except jwt.InvalidTokenError:
        # Token无效
        return None
