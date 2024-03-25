# -*- coding: utf-8 -*-
import traceback
from typing import Iterator
from peewee import ModelSelect, Model
from api_result import ApiResult
from flask import Flask, Blueprint, Request
from playhouse.shortcuts import model_to_dict

from .json_provider import JSONProvider
from .request import FlaskRequest

class FlaskApp(Flask):

    json_provider_class = JSONProvider

    request_class = FlaskRequest

    def get(self, rule, **options):
        return self.route(rule, methods=['GET'], **options)

    def post(self, rule, **options):
        return self.route(rule, methods=['POST'], **options)

    def make_response(self, rv):

        if isinstance(rv, (Iterator, ModelSelect)):
            rv = list(rv)

        if isinstance(rv, (list, dict)) or rv is None:
            rv = ApiResult.success(rv)

        if isinstance(rv, ApiResult):
            rv = rv.to_dict()

        return super().make_response(rv)

class BlueprintApp(Blueprint):
    def get(self, rule, **options):
        return self.route(rule, methods=['GET'], **options)

    def post(self, rule, **options):
        return self.route(rule, methods=['POST'], **options)


class BlueprintAppApi(BlueprintApp):
    """API统一处理"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_error_handler(Exception, self._error_handler)

    def _error_handler(self, e):
        print('@BlueprintAppApi.errorhandler')
        traceback.print_exc()

        result = ApiResult.failure(msg=str(e))

        return result
