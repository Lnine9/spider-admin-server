import json

from model.reslover import Resolver
from model.spider_info import SpiderInfo
from model.spider_response import SpiderResponse
from utils.id import generate_uuid


class SpiderService:
    def __init__(self):
        pass

    @classmethod
    def get_basic_info(self, spider_id):
        spider_info = SpiderInfo.select().where(SpiderInfo.model_id == spider_id).first()
        id_list = json.loads(spider_info.resolvers)
        if spider_info:
            resolvers = Resolver.select().where(Resolver.id.in_(id_list))
            result = {
                'info': spider_info,
                'resolvers': resolvers,
            }
            return result

    @classmethod
    def add_spider_info(self, form):
        spider_info = SpiderInfo()
        spider_info.id = generate_uuid()
        spider_info.name = form['name']
        spider_info.an_type = form['an_type']
        spider_info.enable = 0
        spider_info.discription = form['discription']
        spider_info.section_page_size = form['section_page_size']
        spider_info.callback = form['callback']
        spider_info.method = form['method']
        spider_info.body = form['body']
        spider_info.url = form['url']
        spider_info.base_path = form['base_path']
        spider_info.resolvers = json.dumps(form['resolvers'])
        spider_info.save()
        return spider_info.id

    @classmethod
    def update_spider_info(self, form):
        spider_info = SpiderInfo.select().where(SpiderInfo.id == form['id']).first()
        spider_info.name = form['name']
        spider_info.an_type = form['an_type']
        spider_info.enable = 0
        spider_info.discription = form['discription']
        spider_info.section_page_size = form['section_page_size']
        spider_info.callback = form['callback']
        spider_info.method = form['method']
        spider_info.body = form['body']
        spider_info.url = form['url']
        spider_info.base_path = form['base_path']
        spider_info.resolvers = json.dumps(form['resolvers'])
        spider_info.save()

    @classmethod
    def delete_spider_info(self, id):
        SpiderInfo.delete().where(SpiderInfo.id == id).execute()
        return True

    @classmethod
    def upload_file(self, request, path):
        resolver = Resolver()
        resolver.id = generate_uuid()
        resolver.name = request.form['name']
        resolver.type = request.form['type']
        resolver.class_name = request.form['class_name']
        resolver.discription = request.form['discription']
        resolver.class_path = path
        resolver.save()
