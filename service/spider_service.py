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
        spider_info = SpiderInfo.select().where(SpiderInfo.id == spider_id).first()
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
        spider_info = SpiderInfo().create()
        spider_info.name = form.get('name')
        spider_info.main_class = form.get('main_class')
        spider_info.an_type = form.get('an_type')
        spider_info.enable = 1
        spider_info.description = form.get('description')
        spider_info.callback = 'parse'
        spider_info.method = form.get('method')
        spider_info.body = form.get('body')
        spider_info.url = form.get('url')
        resolvers = form.get('resolvers')
        if resolvers is None or resolvers == '':
            resolvers = []
        spider_info.resolvers = json.dumps(resolvers)
        spider_info.crawl_speed = form.get('crawl_speed')
        spider_info.save()
        result = {
            'spider_id': spider_info.id,
            'spider_name': spider_info.name
        }
        return result

    @classmethod
    def update_spider_info(self, form):
        spider_info = SpiderInfo.select().where(SpiderInfo.id == form['id']).first()
        spider_info.name = form.get('name')
        spider_info.main_class = form.get('main_class')
        spider_info.an_type = form.get('an_type')
        spider_info.enable = 1
        spider_info.description = form.get('description')
        spider_info.callback = form.get('callback')
        spider_info.method = form.get('method')
        spider_info.body = form.get('body')
        spider_info.url = form.get('url')
        resolvers = form.get('resolvers')
        if resolvers is None or resolvers == '':
            resolvers = []
        spider_info.resolvers = json.dumps(resolvers)
        spider_info.crawl_speed = form.get('crawl_speed')
        spider_info.save()

    @classmethod
    def delete_spider_info(self, id):
        SpiderInfo.delete().where(SpiderInfo.id == id).execute()
        return True

    @classmethod
    def upload_file(self, request, path):
        resolver = Resolver().create(id=generate_uuid())
        resolver.name = request.form.get('name')
        resolver.type = request.form.get('type')
        resolver.class_name = request.form.get('class_name')
        resolver.discription = request.form.get('discription')
        resolver.class_path = path
        res = resolver.save()
        result = {
            'resolver_id': resolver.id,
            'resolver_name': resolver.name
        }
        return result

    @classmethod
    def get_file_info(self):
        resolver = Resolver().select()
        return {"resolvers": resolver}

    @classmethod
    def get_spider_list(self, page_no=1, page_size=10):
        spider_info = SpiderInfo().select().where(SpiderInfo.enable == 1).paginate(page_no, page_size)
        total = SpiderInfo.select().where(SpiderInfo.enable == 1).count()
        return {"spider_info": spider_info, "total": total}


    @classmethod
    def add_resolver(cls, form):
        resolver = Resolver().create()
        resolver.name = form.get('name')
        resolver.type = form.get('type')
        resolver.class_name = form.get('class_name')
        resolver.discription = form.get('discription')
        resolver.class_path = form.get('class_path')
        resolver.version_no = 1
        resolver.save()
        return {"resolver_id": resolver.id}

    @classmethod
    def delete_resolver(cls, form):
        id = form.get('id')
        Resolver.delete().where(Resolver.id == id).execute()

    @classmethod
    def resolver_list(cls):
        resolver = Resolver().select().dicts()
        return {"list": resolver, "total": len(resolver)}
