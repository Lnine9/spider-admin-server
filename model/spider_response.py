from model.reslover import Resolver
from model.spider_info import SpiderInfo


class SpiderResponse:
    info:SpiderInfo
    resolvers: list[Resolver]
