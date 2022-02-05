from __future__ import annotations

import configparser
import json

import allure
import pytest

from framework.utils.database_utils.sql_server_connector import SqlServerConnector
from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.logger import Logger
from framework.utils.project_path_utils import ProjectPathUtils
from framework.utils.database_utils.database_cleaner import DatabaseCleaner
from test.tests.product import Product


@pytest.fixture(scope="session")
def read_database_prop():
    Logger.info('Чтение конфиг-файла для доступа к бд')
    config = configparser.ConfigParser()
    config.read(ProjectPathUtils.get_path_relative_to_project_dir("test/resources/database.env"))
    return config


@pytest.fixture(scope='session')
def read_tests_data_full():
    Logger.info('Чтение файла данных для тестов')
    filepath_relative = "test/resources/berkut_tests_data.json"
    filepath = ProjectPathUtils.get_path_relative_to_project_dir(filepath_relative)
    with open(filepath) as json_data:
        return json.load(json_data)


@pytest.fixture()
def read_tests_data_by_test_name(read_tests_data_full, request):
    test_name = request.node.name
    return read_tests_data_full[test_name]


@pytest.fixture(scope="session", autouse=True)
def connect_database(read_database_prop):
    with allure.step("Подключение к базе данных"):
        db_config = read_database_prop
        connector = SqlServerConnector()
        connection = connector.connect(host=db_config.get('DB', 'host'),
                                       username=db_config.get('DB', 'username'),
                                       password=db_config.get('DB', 'password'),
                                       port=db_config.get('DB', 'port'),
                                       database=db_config.get('DB', 'database')
                                       )
        SqlServerExecutor().set_cursor(connection)
    Logger.info('Подключено к БД')
    yield

    connection.close()


@pytest.fixture()
def activate_subscriber(get_product, request) -> Product:
    Logger.info(f'{request.node.name}: вызван activate_subscriber')
    get_product.activate_subscriber()
    return get_product


@pytest.fixture()
def get_product(read_tests_data_full, request) -> Product:
    Logger.info(f'{request.node.name}: вызван get_product')
    product = Product()
    product.create_product(read_tests_data_full)

    yield product

    Logger.info('Удаление продукта из БД')
    product.delete_from_db()


@pytest.fixture
def delete_junk_from_db() -> None:
    yield
    Logger.info('Удаление из БД других созданных строк')
    DatabaseCleaner().delete_all_junk()

