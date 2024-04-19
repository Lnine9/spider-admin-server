import os
import sys

from flask import request
from werkzeug.utils import secure_filename

from service.spider_service import SpiderService
from utils.JWT_token import decode_jwt_token
from utils.flask_ext.flask_app import BlueprintAppApi

spider_api = BlueprintAppApi(name="spider", import_name=__name__)

"""
获取基本信息
:return:
"""


@spider_api.get("/baseInfo")
def get_basic_info():
    spider_id = request.args.get("spider_id")
    return SpiderService.get_basic_info(spider_id)

@spider_api.get("/getSpiderList")
def get_spider_list():
    return SpiderService.get_spider_list()

"""
新增爬虫基本信息
:return:
"""


@spider_api.post("/add")
def add_spider_info():
    return SpiderService.add_spider_info(request.form)




@spider_api.post("/update")
def update_spider_info():
    return SpiderService.update_spider_info(request.form)


@spider_api.post("/delete")
def delete_spider_info():
    id = request.form.get("id")
    return SpiderService.delete_spider_info(id)


"""
爬虫文件上传
:return:
"""


@spider_api.post("/upload")
def upload_file():
    file = request.files['MultiDict']
    user_name = decode_jwt_token(request.headers.get('Authorization'))['user_name']
    pre_path = "/spiders/"+user_name+"/"
    path = pre_path + f"{secure_filename(file.filename)}"
    os.makedirs(os.path.dirname(pre_path), exist_ok=True)
    file.save(path)
    return SpiderService.upload_file(request, path)

@spider_api.get("/getFileInfo")
def get_file_info():
    return SpiderService.get_file_info()