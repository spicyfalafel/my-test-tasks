import json
from types import SimpleNamespace


class JsonUtils(object):

    @staticmethod
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            print(e)
            return False
        return True

    @staticmethod
    def from_json_to_obj(json_post):
        return json.loads(json_post, object_hook=lambda d: SimpleNamespace(**d))

    @staticmethod
    def from_json_to_dict(text):
        return json.loads(text)

    @staticmethod
    def from_dict_to_json(dict, indent_units=4):
        return json.dumps(dict, indent=indent_units)
