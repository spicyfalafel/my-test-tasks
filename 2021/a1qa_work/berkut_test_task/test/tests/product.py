from datetime import datetime

import allure

from framework.utils.logger import Logger
from framework.utils.random_inputs import RandomInputs
from framework.utils.string_utils import random_string
from test.models.tables.client_balance_table import ClientBalanceTable
from test.models.tables.client_table import ClientTable
from test.models.tables.service_table import ServiceTable
from test.models.tables.subs_service_table import SubsServiceTable
from test.models.tables.subscriber_table import SubscriberTable
from test.models.tables.tariff_service_table import TariffServiceTable
from test.models.tables.tariff_table import TariffTable
from test.steps.steps import Steps


class Product(object):
    service: ServiceTable
    tariff: TariffTable
    tariff_service: TariffServiceTable
    client: ClientTable
    subscriber: SubscriberTable
    subs_service: SubsServiceTable
    client_balance: ClientBalanceTable

    def create_product(self, tests_data):
        with allure.step('Создать услугу SUMM_INCL. Зафиксировать id'):
            service_price = tests_data["test_create_subscriber"]["SUMM_INCL1"]
            service_db = Steps.create_service(service_price)

        with allure.step('Создать ТП SUMM_INCL. Зафиксировать id.'):
            tariff_price = tests_data["test_create_subscriber"]["SUMM_INCL2"]
            tariff_model = TariffTable(name=random_string(), price=tariff_price,
                                       creation_date=datetime.now())
            tariff_id = tariff_model.add_to_db(delete_after_test=True)
            Logger.info(f'Id нового тарифа {tariff_id}')
            tariff_db = TariffTable.get_by_id(tariff_id)

        with allure.step('Добавить услугу на ТП'):
            tariff_service_model = TariffServiceTable(tariff_id=tariff_db.id, service_id=service_db.id,
                                                      creation_date=datetime.now())
            tariff_service_model.add_service_to_tariff(delete_after_test=True)
            tariff_services_db = TariffServiceTable.get_by_service_and_tariff_ids(tariff_id, service_db.id)
            Logger.info('Услуга добавлена на тарифный план')

        with allure.step('Создать клиента CLNT_TYPE_ID, BALANCE. Зафиксировать Id'):
            clnt_type_id = tests_data["test_create_subscriber"]["CLNT_TYPE_ID"]
            balance = tests_data["test_create_subscriber"]["BALANCE_SUMM"]
            client_model = ClientTable(name=random_string(), cre_date=datetime.now(), client_type_id=clnt_type_id)
            client_id = client_model.create(clnt_type_id, balance, delete_after_test=True)
            Logger.info(f'Клиент создан с id {client_id}')
            client_db = client_model.get_by_id(client_id)
            balance_db = ClientBalanceTable.get_by_client_id(client_id, delete_after_test=True)

        with allure.step('Создать абонента CLNT_ID, TRPL_ID. Зафиксировать id'):
            subscriber_model = SubscriberTable(name=random_string(), clnt_id=client_id, trpl_id=tariff_id,
                                               cre_date=datetime.now(), msisdn=RandomInputs.random_phone_number())
            subscriber_model.create(delete_after_test=True)
            Logger.info(f'Абонент создан с id {subscriber_model.id}')
            subscriber_db = SubscriberTable.get_by_id(subscriber_model.id)

        with allure.step('Проверить услуги в таблице SUBS_SERVICE'):
            serv_stat_id = tests_data["test_create_subscriber"]["EXPECTED_SERV_STAT_ID"]

            subs_service_model = SubsServiceTable(subs_id=subscriber_db.id, serv_id=service_db.id,
                                                  serv_stat_id=serv_stat_id)
            subs_service_db = SubsServiceTable.get_by_fields_ids(subs_service_table=subs_service_model,
                                                                 delete_after_test=True)

        self.service = service_db
        self.tariff = tariff_db
        self.tariff_service = tariff_services_db
        self.client = client_db
        self.subscriber = subscriber_db
        self.subs_service = subs_service_db
        self.client_balance = balance_db
        self.refresh_all()

    def activate_subscriber(self):
        self.subscriber.activate()
        self.refresh_all()

    def refresh_all(self):
        self.service = self.service.refresh()
        self.tariff = self.tariff.refresh()
        self.tariff_service = self.tariff_service.refresh()
        self.client = self.client.refresh()
        self.subscriber = self.subscriber.refresh()
        self.subs_service = self.subs_service.refresh()
        self.client_balance = self.client_balance.refresh()

    def delete_from_db(self):
        self.tariff_service.delete()
        self.subs_service.delete_by_sub_id(self.subscriber.id)
        self.service.delete()
        self.subscriber.delete()
        self.tariff.delete()
        self.client_balance.delete()
        self.client.delete()
