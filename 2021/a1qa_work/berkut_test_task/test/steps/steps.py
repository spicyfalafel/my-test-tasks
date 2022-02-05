from datetime import datetime

import allure
from hamcrest import assert_that, equal_to, close_to

from framework.asserts.asserts import Asserts
from framework.utils.logger import Logger
from framework.utils.string_utils import random_string
from test.constants import DatabasePrecision
from test.models.tables.client_balance_table import ClientBalanceTable
from test.models.tables.service_orders_table import ServiceOrdersTable
from test.models.tables.service_table import ServiceTable
from test.models.tables.subs_service_table import SubsServiceTable


class Steps:
    @staticmethod
    def set_balance(client_balance, summ_to_upd):
        client_balance.update_balance_summ(summ_to_upd)
        balance_summ_db = ClientBalanceTable.get_balance_summ(client_balance.clnt_id)
        assert_that(balance_summ_db, equal_to(summ_to_upd), 'BALANCE_SUMM отличается')
        return balance_summ_db

    @staticmethod
    def create_service(summ_incl):
        service_model = ServiceTable(name=random_string(), price=summ_incl,
                                     creation_date=datetime.now())

        service_id = service_model.add_to_db(delete_after_test=True)
        Logger.info(f'Id новой услуги {service_id}')
        service_db = ServiceTable.get_by_id(service_id)
        assert_that(service_db, equal_to(service_model))
        return service_db

    @staticmethod
    def check_balance(client_balance, balance_summ_exp, bal_stat_id_exp):
        client_balance = client_balance.refresh()
        Asserts.assert_has_entries(client_balance, bal_stat_id=bal_stat_id_exp)
        assert_that(client_balance.balance_summ, close_to(balance_summ_exp, delta=DatabasePrecision.MONEY_PRECISION))

    @staticmethod
    def check_service_status(subs_service, serv_stat_id_exp):
        service = subs_service.refresh()
        assert_that(service.serv_stat_id, equal_to(serv_stat_id_exp))

    @staticmethod
    def check_service_is_on_sub(serv_id, subs_id, serv_stat_id_exp):
        subs_service_db2 = SubsServiceTable.get_by_fields_ids(serv_id=serv_id,
                                                              subs_id=subs_id)
        assert_that(subs_service_db2.serv_stat_id, equal_to(serv_stat_id_exp))

    @staticmethod
    def activate_sub_with_success(subscriber, subs_stat_id_exp):
        subscriber.activate()
        subscriber = subscriber.refresh()
        assert_that(subscriber.subs_stat_id, equal_to(subs_stat_id_exp),
                    f'SUBS_STAT_ID отличается от ожидаемого')

    @staticmethod
    def check_subscriber_status(subscriber, exp_subs_stat_id):
        subscriber = subscriber.refresh()
        assert_that(subscriber.subs_stat_id, equal_to(exp_subs_stat_id),
                    'статус абонента SUBS_STAT_ID имеет другое значение')

    @staticmethod
    def connect_service_and_subscriber_successfully(serv_id, subs_id, serv_action_id):
        service_orders_model = ServiceOrdersTable(subs_id=subs_id, service_id=serv_id,
                                                  serv_action_id=serv_action_id, creation_date=datetime.now())
        error_add = service_orders_model.add_service_to_subscriber(delete_after_test=True)
        assert_that(error_add is None, f'Ошибка при создании заказа: {error_add}')
