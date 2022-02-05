import json
from types import SimpleNamespace

from framework.utils.APIUtils import API_utils
from framework.utils.json_utils import JsonUtils
from tests.models.post import Post
from tests.models.user import User
from tests.task3urls import Task3Urls


class TypecodeApi(object):

    # posts

    @staticmethod
    def post_post(post):
        body = {'userId': post.user_id, 'title': post.title, 'body': post.body}
        code, json_post = API_utils.POST(url=Task3Urls.POSTS, body=body, dict_ans=False)
        post = JsonUtils.from_json_to_obj(json_post)
        return code, post

    @staticmethod
    def get_posts():
        code, posts_dict = API_utils.GET(url=Task3Urls.POSTS)
        posts = []
        for post in posts_dict:
            posts.append(Post(post["userId"], post["id"], post["title"], post["body"]))
        return code, posts

    @staticmethod
    def get_post(post_id):
        code, post_text = API_utils.GET(url=Task3Urls.POSTS + "/" + str(post_id), dict_ans=False)
        post = JsonUtils.from_json_to_obj(post_text)
        if post != SimpleNamespace():
            return code, post
        else:
            return code, "{}"

    # users

    @staticmethod
    def get_users():
        code, users_text = API_utils.GET(url=Task3Urls.USERS, dict_ans=False)
        users = []
        for user_data in JsonUtils.from_json_to_dict(users_text):
            users.append(User(user_data))
        return code, users

    @staticmethod
    def get_user(user_id):
        code, user_text = API_utils.GET(url=Task3Urls.USERS + "/" + str(user_id), dict_ans=False)
        return code, User(JsonUtils.from_json_to_dict(user_text))

    @staticmethod
    def get_user_by_id_from_json(users_json, id):
        code, data = API_utils.get_by_val_in_array(users_json, "id", id)
        return code, User(data)

    @staticmethod
    def post_user(user):
        body = json.dumps(user.data.__dict__)
        code, post_json = API_utils.POST(url=Task3Urls.USERS, body=body)
        return code, JsonUtils.from_json_to_obj(post_json)
