from flask import request

from service.spider_service import SpiderService
from utils.flask_ext.flask_app import BlueprintAppApi

spider_api = BlueprintAppApi(name="spider", import_name=__name__)


@spider_api.get("/baseInfo")
def get_basic_info():
    """
    获取基本信息
    :return:
    """
    spider_id = request.args.get("spider_id")
    SpiderService.get_basic_info(spider_id)
    return {"code": 200, "msg": "success"}
