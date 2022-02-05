from __future__ import annotations

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.datetime_util import DatetimeUtil
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable
from test.models.tables.subscriber_table import SubscriberTable


class ServiceTable(BaseTable):
    _get_by_id = """
              SELECT * FROM SERVICE
              WHERE SERV_ID = ?
          """
    _get_all = f"""
        SELECT * FROM SERVICE
    """
    _add_one = f"""
        INSERT INTO
        SERVICE 
        (SERV_ID, NAME, CRE_DATE, SUMM_INCL)
        VALUES
        (?,?,?,?)"""
    _max_id = "select max(SERV_ID) from SERVICE"
    _delete_one = "delete from SERVICE WHERE SERV_ID = ?;"
    del_priority = DeletePriorityConsts.SERVICE

    def __init__(self, name, creation_date, price, comment=None, service_id=None) -> None:
        super().__init__(service_id)
        self.name = name
        self.creation_date = creation_date
        self.price = price
        self.comment = comment

    @staticmethod
    def get_services() -> tuple[ServiceTable]:
        db = SqlServerExecutor()
        services_tuples = db.get_data_all(ServiceTable._get_all)
        return tuple(ServiceTable.from_tuple(s) for s in services_tuples)

    def __eq__(self, other) -> bool:
        return (other.name.strip() == self.name.strip()
                and DatetimeUtil.datetimes_are_equal_sec_precision(other.creation_date, self.creation_date)
                and other.price == self.price
                and other.comment == self.comment)

    def ordered(self):
        return self.id, self.name, self.creation_date, self.price, self.comment

    @staticmethod
    def from_tuple(tupl) -> ServiceTable:
        return ServiceTable(service_id=tupl[0],
                            name=tupl[1],
                            creation_date=tupl[2],
                            price=tupl[3],
                            comment=tupl[4])
