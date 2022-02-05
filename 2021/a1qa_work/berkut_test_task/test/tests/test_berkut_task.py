from datetime import datetime

import allure
import pytest
from hamcrest import equal_to, assert_that, contains_string, none

from framework.asserts.asserts import Asserts
from framework.utils.logger import Logger
from framework.utils.random_inputs import RandomInputs
from framework.utils.string_utils import random_string
from test.models.tables.client_balance_table import ClientBalanceTable
from test.models.tables.client_table import ClientTable
from test.models.tables.service_orders_table import ServiceOrdersTable
from test.models.tables.subs_service_table import SubsServiceTable
from test.models.tables.subscriber_table import SubscriberTable
from test.models.tables.tariff_service_table import TariffServiceTable
from test.models.tables.tariff_table import TariffTable
from test.steps.steps import Steps
from test.tests.product import Product


class TestBerkutTask:
    # 1
    def test_create_subscriber(self, read_tests_data_by_test_name, delete_junk_from_db):
        tests_data = read_tests_data_by_test_name

        with allure.step('Создать услугу SUMM_INCL. Зафиксировать id'):
            service_price = tests_data["SUMM_INCL1"]
            service_db = Steps.create_service(service_price)

        with allure.step('Создать ТП SUMM_INCL. Зафиксировать id.'):
            tariff_price = tests_data["SUMM_INCL2"]
            tariff_model = TariffTable(name=random_string(), price=tariff_price, creation_date=datetime.now())
            tariff_id = tariff_model.add_to_db(delete_after_test=True)
            Logger.info(f'Id нового тарифа {tariff_id}')
            tariff_db = TariffTable.get_by_id(tariff_id)

            assert_that(tariff_db, equal_to(tariff_model))

        with allure.step('Добавить услугу на ТП'):
            tariff_service_model = TariffServiceTable(tariff_id=tariff_db.id, service_id=service_db.id,
                                                      creation_date=datetime.now())
            tariff_service_model.add_service_to_tariff(delete_after_test=True)
            tariff_services_db = TariffServiceTable.get_by_service_and_tariff_ids(tariff_id, service_db.id)

            assert_that(tariff_services_db.tariff_id, equal_to(tariff_id), 'id тарифа не такое, как в шаге 2')
            assert_that(tariff_services_db.service_id, equal_to(service_db.id), 'id сервиса не такое, как в шаге 1')
            Logger.info('Услуга добавлена на тарифный план')

        with allure.step('Создать клиента CLNT_TYPE_ID, BALANCE. Зафиксировать Id'):
            clnt_type_id = tests_data["CLNT_TYPE_ID"]
            balance = tests_data["BALANCE_SUMM"]
            client_model = ClientTable(name=random_string(), cre_date=datetime.now(), client_type_id=clnt_type_id)
            client_id = client_model.create(clnt_type_id, balance, delete_after_test=True)
            Logger.info(f'Клиент создан с id {client_id}')

            client_db = client_model.get_by_id(client_id)
            assert_that(client_db, equal_to(client_model))

            balance_db = ClientBalanceTable.get_by_client_id(client_id, delete_after_test=True)
            assert_that(balance_db.balance_summ, balance, 'балансы не совпадают')

        with allure.step('Создать абонента CLNT_ID, TRPL_ID. Зафиксировать id'):
            expected_clnt_status = tests_data["EXPECTED_CLNT_STATUS"]
            subscriber_model = SubscriberTable(name=random_string(), clnt_id=client_id, trpl_id=tariff_id,
                                               cre_date=datetime.now(), msisdn=RandomInputs.random_phone_number())
            subscriber_model.create(delete_after_test=True)
            Logger.info(f'Абонент создан с id {subscriber_model.id}')
            subscriber_db = SubscriberTable.get_by_id(subscriber_model.id)
            assert_that(subscriber_db.subs_stat_id, equal_to(expected_clnt_status), 'SUBS_STAT_ID из БД отличался')
            assert_that(subscriber_db.clnt_id, equal_to(subscriber_model.clnt_id), 'CLNT_ID из БД отличался')

        with allure.step('Проверить услуги в таблице SUBS_SERVICE'):
            serv_stat_id = tests_data["EXPECTED_SERV_STAT_ID"]

            subs_service_model = SubsServiceTable(subs_id=subscriber_db.id, serv_id=service_db.id,
                                                  serv_stat_id=serv_stat_id)
            subs_service_db = SubsServiceTable.get_by_fields_ids(subs_service_table=subs_service_model,
                                                                 delete_after_test=True)
            Asserts.assert_has_entries(subs_service_db, serv_id=subs_service_model.serv_id,
                                       subs_id=subs_service_model.subs_id,
                                       serv_stat_id=subs_service_model.serv_stat_id)

    # 2
    # Предусловие: выполнить шаги тестового сценария: 1. Создание абонента с базовым ТП
    def test_subscriber_is_activated(self, get_product: Product, read_tests_data_by_test_name):
        tests_data = read_tests_data_by_test_name
        p = get_product

        with allure.step('Выполнить активацию абонента'):
            subs_stat_id_exp = tests_data["SUBS_STAT_ID"]
            Steps.activate_sub_with_success(p.subscriber, subs_stat_id_exp)

        with allure.step('Проверить статус услуги'):
            serv_stat_id_exp = tests_data["SERV_STAT_ID"]
            Steps.check_service_status(p.subs_service, serv_stat_id_exp)

        with allure.step('Проверить баланс клиента'):
            bal_stat_id_exp = tests_data["BAL_STAT_ID"]
            balance_summ_exp = tests_data["BALANCE_SUMM"]
            Steps.check_balance(p.client_balance, balance_summ_exp, bal_stat_id_exp)

    # 3
    # Предусловие: выполнить шаги тестового сценария: 1. Создание абонента с базовым ТП
    def test_subscriber_activation_error(self, get_product: Product, read_tests_data_by_test_name):
        tests_data = read_tests_data_by_test_name
        p = get_product

        with allure.step('Установить баланс клиента'):
            summ_to_upd = tests_data["BALANCE_SUMM"]
            Steps.set_balance(p.client_balance, summ_to_upd)

        with allure.step('Выполнить активацию абонента '):
            error = p.subscriber.activate()
            assert_that(error, 'не было ошибки')
            assert_that(error, contains_string('ERROR'), 'строка не содержала ERROR')
            subscriber = p.subscriber.refresh()

            subs_stat_id_exp = tests_data["SUBS_STAT_ID"]
            assert_that(subscriber.subs_stat_id, equal_to(subs_stat_id_exp),
                        'значение SUBS_STAT_ID в БД отличается от ожидаемого')
        with allure.step('Проверить статус услуги'):
            subs_stat_id_exp = tests_data["SERV_STAT_ID"]
            Steps.check_service_status(p.subs_service, subs_stat_id_exp)

        with allure.step('Проверить баланс клиента'):
            bal_stat_id_exp = tests_data["BAL_STAT_ID"]
            bal_summ_exp = tests_data["BALANCE_SUMM2"]
            Steps.check_balance(p.client_balance, bal_summ_exp, bal_stat_id_exp)

    # 4
    # Предусловие: выполнить шаги тестового сценария: 1. Создание абонента с базовым ТП
    def test_block_subscriber_while_activation(self, get_product: Product,
                                               read_tests_data_by_test_name):
        product = get_product
        tests_data = read_tests_data_by_test_name

        with allure.step('Установить баланс клиента'):
            balance_summ = tests_data['BALANCE_SUMM']
            Steps.set_balance(product.client_balance, balance_summ)

        with allure.step('Выполнить активацию абонента '):
            subs_stat_id_exp = tests_data['SUBS_STAT_ID']
            Steps.activate_sub_with_success(product.subscriber, subs_stat_id_exp)

        with allure.step('Проверить статус услуги'):
            serv_stat_id_exp = tests_data['SERV_STAT_ID']
            Steps.check_service_status(product.subs_service, serv_stat_id_exp)

        with allure.step('Проверить баланс клиента'):
            bal_stat_id_exp = tests_data['BAL_STAT_ID']
            bal_sum_exp = tests_data['BALANCE_SUMM2']
            Steps.check_balance(product.client_balance, bal_sum_exp, bal_stat_id_exp)

    # 5, 6, 8
    # Предусловие: выполнить шаги тестового сценария: 2. Успешная активация абонента
    @pytest.mark.parametrize(
        "balance, serv_summ, serv_action_id, exp_serv_stat_id, exp_subs_stat_id,"
        "exp_bal_stat_id, exp_bal_summ",
        [(50, 40, 1, 1, 1, 1, 10),
         (40, 40, 1, 1, 3, 3, 0),
         (25, 50, 3, 3, 1, 1, 25)
         ])
    def test_connect_new_service_to_subscriber(self, delete_junk_from_db, activate_subscriber: Product,
                                               balance, serv_summ, serv_action_id, exp_serv_stat_id,
                                               exp_subs_stat_id, exp_bal_stat_id, exp_bal_summ):
        product = activate_subscriber

        with allure.step('Установить баланс клиента'):
            Steps.set_balance(product.client_balance, balance)

        with allure.step('Создать услугу SUMM INCL. Зафиксировать id'):
            service_model = Steps.create_service(serv_summ)

        with allure.step('Выполнить подключение услуги абоненту: 1.Создать заказ на подключение услуги(ServiceOrder): '
                         '2.Выполнить обработку заявок(WorkerOrders) '):
            Steps.connect_service_and_subscriber_successfully(service_model.id, product.subscriber.id, serv_action_id)

        with allure.step('Проверить, что новая услуга подключена абоненту'):
            Steps.check_service_is_on_sub(service_model.id, product.subscriber.id, exp_serv_stat_id)

        with allure.step('Проверить статус абонента '):
            Steps.check_subscriber_status(product.subscriber, exp_subs_stat_id)
        with allure.step('Проверить баланс клиента'):
            Steps.check_balance(product.client_balance, exp_bal_summ, exp_bal_stat_id)

    # 7
    # Предусловие: выполнить шаги тестового сценария: 2. Успешная активация абонента
    def test_connect_service_with_insufficient_balance(self, delete_junk_from_db,
                                                       activate_subscriber, read_tests_data_by_test_name):
        product = activate_subscriber
        tests_data = read_tests_data_by_test_name

        with allure.step('Установить баланс клиента'):
            balance = tests_data['BALANCE_SUMM']
            Steps.set_balance(product.client_balance, balance)

        with allure.step('Создать услугу SUMM INCL. Зафиксировать id'):
            serv_summ = tests_data['SUMM_INCL']
            service_model = Steps.create_service(serv_summ)

        with allure.step('Выполнить подключение услуги абоненту: 1.Создать заказ на подключение услуги:'
                         ' 2.Выполнить обработку заявок '):
            serv_action_id = tests_data['SERV_ACTION_ID']

            service_orders_model = ServiceOrdersTable(subs_id=product.subscriber.id, service_id=service_model.id,
                                                      serv_action_id=serv_action_id, creation_date=datetime.now())
            error_add = service_orders_model.add_service_to_subscriber(delete_after_test=True)
            assert_that(error_add is not None, 'Нет ошибки при создании заказа')

        with allure.step('Проверить что услуги нет на абоненте '):
            subs_service_db = SubsServiceTable.get_by_fields_ids(serv_id=service_model.id,
                                                                 subs_id=product.subscriber.id,
                                                                 serv_stat_id=None)

            assert_that(subs_service_db, none(), 'есть запись новой услуги абонента в SUBS_SERVICE')

        with allure.step('Проверить статус абонента'):
            exp_subs_stat_id = tests_data['SUBS_STAT_ID']
            Steps.check_subscriber_status(product.subscriber, exp_subs_stat_id)

        with allure.step('Проверить, что баланс клиента не изменился'):
            bal_stat_id_exp = tests_data['BAL_STAT_ID']
            bal_summ_exp = tests_data['BALANCE_SUMM2']
            Steps.check_balance(product.client_balance, bal_summ_exp, bal_stat_id_exp)

    # 9
    # Предусловие: выполнить шаги тестового сценария: 2. Успешная активация абонента
    def test_connect_several_new_services(self, delete_junk_from_db,
                                          activate_subscriber: Product, read_tests_data_by_test_name):
        product = activate_subscriber
        tests_data = read_tests_data_by_test_name

        with allure.step('Установить баланс клиента'):
            balance = tests_data['BALANCE_SUMM']
            Steps.set_balance(product.client_balance, balance)

        with allure.step('Создать услугу SUMM INCL. Зафиксировать id'):
            serv_summ1 = tests_data['SUMM_INCL1']
            service_model1 = Steps.create_service(serv_summ1)

        with allure.step('Создать услугу SUMM INCL. Зафиксировать id'):
            serv_summ2 = tests_data['SUMM_INCL1']
            service_model2 = Steps.create_service(serv_summ2)

        with allure.step('1.Создать заказ на подключение услуги (2): SERV_ID = (2).id SUBS_ID = (precondition).subs.id'
                         'SERV_ACTION_ID 2.Создать заказ на блокирование услуги(3): SERV_ID = (2).id '
                         'SUBS_ID = (precondition).subs.id SERV_ACTION_ID 3.Выполнить обработку заявок '):
            serv_action_id1 = tests_data['SERV_ACTION_ID1']
            service_orders_model1 = ServiceOrdersTable(subs_id=product.subscriber.id, service_id=service_model1.id,
                                                       serv_action_id=serv_action_id1, creation_date=datetime.now())
            error_connect = service_orders_model1.add_service_to_subscriber(delete_after_test=True)
            assert_that(error_connect is None, f'Ошибка при создании заказа: {error_connect}')

            serv_action_id2 = tests_data['SERV_ACTION_ID2']
            service_orders_model2 = ServiceOrdersTable(subs_id=product.subscriber.id, service_id=service_model2.id,
                                                       serv_action_id=serv_action_id2, creation_date=datetime.now())
            error_block = service_orders_model2.add_service_to_subscriber(delete_after_test=True)
            assert_that(error_block is None, f'Ошибка при создании заказа: {error_block}')

        with allure.step('Проверить что услуга (2) на абоненте '):
            serv_stat_id1_exp = tests_data['SERV_STAT_ID1']
            Steps.check_service_is_on_sub(service_model1.id, product.subscriber.id, serv_stat_id1_exp)

        with allure.step('Проверить что услуга (3) на абоненте '):
            serv_stat_id2_exp = tests_data['SERV_STAT_ID2']
            Steps.check_service_is_on_sub(service_model2.id, product.subscriber.id, serv_stat_id2_exp)

        with allure.step('Проверить статус абонента'):
            exp_subs_stat_id = tests_data['SUBS_STAT_ID']
            Steps.check_subscriber_status(product.subscriber, exp_subs_stat_id)

        with allure.step('Проверить что баланс клиента не изменился'):
            bal_stat_id_exp = tests_data['BAL_STAT_ID']
            bal_summ_exp = tests_data['BALANCE_SUMM2']
            Steps.check_balance(product.client_balance, bal_summ_exp, bal_stat_id_exp)
