import allure

from framework.utils.APIUtils import API_utils
from framework.utils.logger import Logger
from framework.utils.string_utils import StringUtils
from tests.models.post import Post
from tests.task3urls import Task3Urls
from tests.typecode_api import TypecodeApi


class TestTask2(object):

    def test_api(self, create_browser, get_task_data):
        self.task3_data = get_task_data
        with allure.step("Отправить GET запрос для получения всех постов"):

            status, posts = TypecodeApi.get_posts()
            assert status == API_utils.OK_CODE, 'status code is not OK'
            assert all(posts[i].id <= posts[i + 1].id for i in range(len(posts) - 1)) \
                , 'sorting by id expected'

        with allure.step("Отправить GET запрос для получения поста №99"):
            status, post = TypecodeApi.get_post(self.task3_data["existingPostNumber"])
            assert status == API_utils.OK_CODE, 'status code is not OK'
            Logger.info('Checking userId is expected id')
            assert self.task3_data["expectedExistingUserId"] == post.userId, ''
            Logger.info('Checking title and body are not empty')
            assert post.title != "", 'title was empty'
            assert post.body != "", 'body was empty'

        with allure.step("Отправить GET запрос для получения поста №150"):
            status, post = TypecodeApi.get_post(self.task3_data["nonExistingPostNumber"])
            assert status == API_utils.NOT_FOUND_CODE, 'status code is not NOT FOUND'
            Logger.info('Checking if body is empty')
            assert post == "{}", 'body of post was not empty'

        with allure.step("Отправить POST запрос для создания записи"):
            generated_body_key = StringUtils.generate_random()
            generated_title_key = StringUtils.generate_random()
            Logger.info('Sending POST request with generated body and title')
            status, post = TypecodeApi.post_post(Post.without_id(generated_title_key, generated_body_key))
            assert status == API_utils.CREATED_CODE, 'code was not CREATED'

            Logger.info('Checking if title and body keys are the same as expected')
            assert post.title == generated_title_key, 'title is expected to be the same as generated'
            assert post.body == generated_body_key, 'body is expected to be the same as generated'
            Logger.info('Checking if id key in response body')
            assert post.id != "", 'id was empty'

        with allure.step("Отправить GET запрос для получения пользователей"):
            status, users = TypecodeApi.get_users()

            assert status == API_utils.OK_CODE, 'OK code expected'
            expected_user = self.task3_data["step5user"]
            self.user_step5 = next(u for u in users if u.data["id"] == self.task3_data["step5id"])
            Logger.info('Checking if user has expected values')
            assert self.user_step5.data == expected_user, 'expected_user must be equal to user_step5 '

        with allure.step("Отправить GET запрос для получения пользователя 5"):
            status, user_step6 = TypecodeApi.get_user(self.task3_data["step6id"])

            assert status == API_utils.OK_CODE, 'OK code expected'
            Logger.info("Checking if user from step 5 is equal to user from step 6")
            assert user_step6.data == self.user_step5.data, 'user from step 5 must be equal to user from step 6'
