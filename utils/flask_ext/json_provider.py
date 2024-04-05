from datetime import datetime
from peewee import ModelSelect, Model
from playhouse.shortcuts import model_to_dict
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def default_json_encoder(o):
    """
    json 序列化
    :param o:
    :return:
    """
    if isinstance(o, ModelSelect):
        return list(o.dicts())

    if isinstance(o, Model):
        return model_to_dict(o)

    if isinstance(o, datetime):
        return o.timestamp()

    return o

try:
    from flask.json.provider import DefaultJSONProvider, _default
except ImportError:
    class DefaultJSONProvider(object):
        pass


    def _default(o):
        pass


class JSONProvider(DefaultJSONProvider):
    """
    Flask 2.2.2
    """

    @staticmethod
    def default(o):
        ret = default_json_encoder(o)
        if ret is not o:
            return ret

        return _default(o)
