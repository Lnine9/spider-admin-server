from flask import request, redirect
from service.login_service import LoginService
from utils.flask_ext.flask_app import BlueprintAppApi

login_api = BlueprintAppApi(name="sign", import_name=__name__)


@login_api.get('/login')
def login():
    params = request.args.to_dict()
    user_name = params.get('user_name')
    password = params.get('password')
    return LoginService.login(user_name, password)


@login_api.get('/sign')
def sign():
    params = request.args.to_dict()
    user_name = params.get('user_name')
    password = params.get('password')
    return LoginService.sign(user_name, password)


@login_api.get('/logout')
def logout():
    return redirect('/index', code=302, Response=None)
