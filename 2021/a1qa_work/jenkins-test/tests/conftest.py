import json

import allure
import pytest

from jenkinsapi.jenkins import Jenkins

from framework.browser.browser import Browser
from framework.constants import browsers
from framework.utils.logger import Logger
from framework.utils.project_path_utils import ProjectPathUtils
from tests.config.browser import BrowserConfig
from tests.config.browser import Grid


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=BrowserConfig.BROWSER,
                     help="Name of browser")
    parser.addoption("--grid_port", action="store", default=Grid.GRID_PORT,
                     help="Port of remote connection")


@pytest.fixture(scope="session")
def create_browser(request):
    """
        Создание сессии браузера с именем из конфиг файла.
    Args:

    """

    j = Jenkins('http://localhost:8080', 'admin', 'admin')
    job = j.get_job("three")
    build = job.get_last_build()
    parameters = build.get_actions()['parameters']
    browser_from_jenkins = parameters[0]['value']

    with allure.step("Создание сессии браузера"):
        if browser_from_jenkins in [browsers.BROWSER_CHROME, browsers.BROWSER_FIREFOX]:
            Logger.info("Сессия браузера создана с именем браузера из Jenkins")
            browser = browser_from_jenkins
        else:
            Logger.info("Сессия браузера создана с именем браузера из конфиг файла")
            browser = request.config.getoption('--browser')
        Browser.get_browser().set_up_driver(browser_key=browser, grid_port=request.config.getoption('--grid_port'))
        Browser.get_browser().maximize(browser_key=browser)

    yield

    with allure.step("Закрытие сессий всех браузеров"):
        for browser_key in list(Browser.get_browser().get_driver_names()):
            Browser.get_browser().quit(browser_key=browser_key)


@pytest.fixture(autouse=True)
def get_task_data():
    with allure.step("Getting data from task2.json"):
        filepath = ProjectPathUtils.get_path_to_project_dir("resources", "task3_api_testing.json")
        with open(filepath) as json_urls:
            return json.load(json_urls)
