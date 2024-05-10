import json
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
    page_no = int(request.args.get("page_no"))
    page_size = int(request.args.get("page_size"))
    return SpiderService.get_spider_list(page_no, page_size)


"""
新增爬虫基本信息
:return:
"""


@spider_api.post("/add")
def add_spider_info():
    return SpiderService.add_spider_info(json.loads(request.data))


@spider_api.post("/update")
def update_spider_info():
    return SpiderService.update_spider_info(json.loads(request.data))


@spider_api.post("/delete")
def delete_spider_info():
    id = json.loads(request.data)['id']
    return SpiderService.delete_spider_info(id)


@spider_api.post("/add_resolver")
def add_resolver():
    return SpiderService.add_resolver(request.json)

@spider_api.post("/delete_resolver")
def delete_resolver():
    return SpiderService.delete_resolver(request.json)

@spider_api.get("/resolver_list")
def resolver_list():
    return SpiderService.resolver_list()

"""
爬虫文件上传
:return:
"""


@spider_api.post("/upload")
def upload_file():
    file = request.files['MultiDict']
    pre_path = "/spiders/"
    path = pre_path + f"{secure_filename(file.filename)}"
    os.makedirs(os.path.dirname(pre_path), exist_ok=True)
    file.save(path)
    return SpiderService.upload_file(request, path)


@spider_api.get("/getFileInfo")
def get_file_info():
    return SpiderService.get_file_info()
