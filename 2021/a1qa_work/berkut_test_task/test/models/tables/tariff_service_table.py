from __future__ import annotations

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.datetime_util import DatetimeUtil
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable
from framework.utils.database_utils.database_cleaner import DatabaseCleaner


class TariffServiceTable(BaseTable):
    _max_id = "select max(TAR_SERV_ID) from TARIFF_SERVICE;"
    __add_service_to_tariff = f"""
            BEGIN
            DECLARE @id int;
            Execute AddServiceToTrpl @TrplId = ?,
            @ServId = ?,
            @TarServId = @id output
            end
    """

    _get_by_id = "select * from TARIFF_SERVICE WHERE TAR_SERV_ID = ?"
    _get_all = "select * from TARIFF_SERVICE"
    __get_where_tariff_and_service_ids = "select * from TARIFF_SERVICE where TRPL_ID=? and SERV_ID=?;"
    _delete_one = "delete from TARIFF_SERVICE WHERE TAR_SERV_ID = ?"
    del_priority = DeletePriorityConsts.TARIFF_SERVICE

    def __init__(self, tariff_id, service_id, creation_date, tar_serv_id=None) -> None:
        super().__init__(tar_serv_id)
        self.tariff_id = tariff_id
        self.service_id = service_id
        self.creation_date = creation_date

    def __eq__(self, other) -> bool:
        return (other.id == self.id
                and other.client_type_id == self.tariff_id
                and other.name == self.service_id
                and DatetimeUtil.datetimes_are_equal_sec_precision(other.creation_date, self.creation_date))

    def add_service_to_tariff(self, delete_after_test=False) -> None:
        db = SqlServerExecutor()
        db.modify_data(TariffServiceTable.__add_service_to_tariff,
                       self.tariff_id, self.service_id)
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=self, priority=self.del_priority)

    @staticmethod
    def get_by_service_and_tariff_ids(tariff_id: int, service_id: int) -> TariffServiceTable:
        db = SqlServerExecutor()
        data_tuple = db.get_data_one(TariffServiceTable.__get_where_tariff_and_service_ids, tariff_id, service_id)
        return TariffServiceTable.from_tuple(data_tuple)

    @staticmethod
    def from_tuple(tupl) -> TariffServiceTable:
        return TariffServiceTable(tar_serv_id=tupl[0],
                                  tariff_id=tupl[1],
                                  service_id=tupl[2],
                                  creation_date=tupl[3])

    def ordered(self) -> tuple:
        return self.id, self.tariff_id, self.service_id, self.creation_date
