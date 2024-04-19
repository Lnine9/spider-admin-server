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
        spider_info = SpiderInfo().create(id=generate_uuid())
        spider_info.name = form.get('name')
        spider_info.an_type = form.get('an_type')
        spider_info.enable = 0
        spider_info.description = form.get('description')
        spider_info.section_page_size = form.get('section_page_size')
        spider_info.callback = form.get('callback')
        spider_info.method = form.get('method')
        spider_info.body = form.get('body')
        spider_info.url = form.get('url')
        spider_info.base_path = form.get('base_path')
        spider_info.resolvers = json.dumps(form.get('resolvers'))
        spider_info.save()
        result = {
            'spider_id': spider_info.id,
            'spider_name': spider_info.id
        }
        return result

    @classmethod
    def update_spider_info(self, form):
        spider_info = SpiderInfo.select().where(SpiderInfo.id == form['id']).first()
        spider_info.name = form.get('name')
        spider_info.an_type = form.get('an_type')
        spider_info.enable = 0
        spider_info.description = form.get('description')
        spider_info.section_page_size = form.get('section_page_size')
        spider_info.callback = form.get('callback')
        spider_info.method = form.get('method')
        spider_info.body = form.get('body')
        spider_info.url = form.get('url')
        spider_info.base_path = form.get('base_path')
        spider_info.resolvers = json.dumps(form.get('resolvers'))
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
        spider_info = SpiderInfo().select().paginate(page_no, page_size)
        total = SpiderInfo().select().scalar()
        return {"spider_info": spider_info, "total": total}
