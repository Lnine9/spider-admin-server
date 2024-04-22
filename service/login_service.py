import hashlib
from datetime import datetime

from flask import Response

from model.user import User
from utils.JWT_token import generate_jwt_token
from utils.id import generate_uuid


class LoginService:
    def __init__(self):
        pass

    @classmethod
    def login(self, user_name, password):
        if user_name and password:
            query = User.select(User).where(User.user_name == user_name).first()
            if query is None:
                return Response("登录失败", 500)
            if hashlib.sha256(password.encode()).hexdigest() == query.password:
                user = {
                    "id": query.id,
                    "user_name": query.user_name,
                    "state": str(query.state)
                }
                token = generate_jwt_token(user)
                return {"token": token}
        return Response("登录失败", 500)

    @classmethod
    def sign(self, user_name, password):
        if user_name and password:
            query = User.select(User).where(User.user_name == user_name).first()
            if query is not None:
                return {"error""用户存在"}
            user = User.create(
                id=generate_uuid(),
                user_name=user_name,
                password=hashlib.sha256(password.encode()).hexdigest(),
                create_time=datetime.now(),
                state=0
            )
            user.save()
            return {"id": user.id}
