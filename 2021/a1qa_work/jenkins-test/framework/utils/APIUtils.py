import requests

from framework.utils.logger import Logger


class API_utils(object):
    OK_CODE = 200
    NOT_FOUND_CODE = 404
    CREATED_CODE = 201

    @staticmethod
    def log_code(status_code, url):
        if status_code == API_utils.OK_CODE:
            Logger.info(f'{url} OK')
        elif status_code == API_utils.NOT_FOUND_CODE:
            Logger.info(f'{url} NOT FOUND')
        else:
            Logger.info(f"{url} code {status_code}")

    @staticmethod
    def GET(url, dict_ans=True):
        response = requests.get(url)
        API_utils.log_code(response.status_code, url)
        if dict_ans:
            return response.status_code, response.json()
        else:
            return response.status_code, response.text

    @staticmethod
    def POST(url, body="", dict_ans=True):
        response = requests.post(url, data=body)
        API_utils.log_code(response.status_code, url)
        Logger.info(f"{url} code {response.status_code}")
        if dict_ans:
            return response.status_code, response.json()
        else:
            return response.status_code, response.text

    @staticmethod
    def get_by_val_in_array(json_arr, key, value):
        for obj in json_arr:
            print(type(obj))
            print(obj.values())
            for k, v in obj.items():
                if k == key and v == value:
                    return obj
        return {}

    @staticmethod
    def dict_has_same(first_dict, second_dict):
        for k, v in second_dict.items():
            if not (k in first_dict and first_dict[k] == v):
                return False
        return True
