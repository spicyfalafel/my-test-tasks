from __future__ import annotations

from pyodbc import ProgrammingError

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.logger import Logger
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable
from framework.utils.database_utils.database_cleaner import DatabaseCleaner


class ServiceOrdersTable(BaseTable):
    _max_id = "select max(SERV_ORDER_ID) from SERVICE_ORDERS;"
    _get_by_id = "select * from SERVICE_ORDERS WHERE SERV_ORDER_ID = ?"
    _get_all = "select * from SERVICE_ORDERS"
    _delete_all = "delete from SERVICE_ORDERS"
    _delete_one = "delete from SERVICE_ORDERS WHERE SERV_ORDER_ID = ?"
    __add_service_to_subscriber = '''BEGIN
        DECLARE @errmsg nchar(100);
        EXECUTE ServiceOrder	@SubsId = ?, @ServId = ?, @ServActionId = ?, @ErrMsg = @errmsg OUTPUT;
        execute WorkerOrders    @ErrMsg = @errmsg OUTPUT;
        select @ErrMsg;
    end'''
    del_priority = DeletePriorityConsts.SERVICE_ORDERS

    def __init__(self, subs_id, service_id, serv_action_id, creation_date, is_complete=None,
                 serv_order_id=None) -> None:
        super().__init__(serv_order_id)
        self.subs_id = subs_id
        self.service_id = service_id
        self.serv_action_id = serv_action_id
        self.is_complete = is_complete
        self.creation_date = creation_date

    def add_service_to_subscriber(self, delete_after_test=False):
        db = SqlServerExecutor()
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=self, priority=self.del_priority)
        Logger.info(f'Создание заказа на подключение услуги с SERV_ID {self.service_id} и SUBS_ID {self.subs_id}')
        try:
            db.modify_and_get(self.__add_service_to_subscriber,
                              self.subs_id, self.service_id, self.serv_action_id)
            return None
        except ProgrammingError as e:
            return str(e)

    @staticmethod
    def from_tuple(tupl) -> ServiceOrdersTable:
        return ServiceOrdersTable(serv_order_id=tupl[0],
                                  subs_id=tupl[1],
                                  service_id=tupl[2],
                                  serv_action_id=tupl[3],
                                  is_complete=tupl[4],
                                  creation_date=tupl[5])

    def ordered(self) -> tuple:
        return self.id, self.subs_id, self.service_id, self.serv_action_id, self.is_complete, self.creation_date
