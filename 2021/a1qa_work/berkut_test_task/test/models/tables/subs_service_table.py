from __future__ import annotations

from pyodbc import ProgrammingError

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable
from framework.utils.database_utils.database_cleaner import DatabaseCleaner


class SubsServiceTable(BaseTable):
    __get_by_ids = """
        SELECT * FROM SUBS_SERVICE
        WHERE SUBS_ID = ? AND SERV_ID = ? AND SERV_STAT_ID = ?;"""
    __get_by_subs_and_serv_ids = """
        SELECT * FROM SUBS_SERVICE
        WHERE SUBS_ID = ? AND SERV_ID = ?;"""
    _get_by_id = """
        SELECT * FROM SUBS_SERVICE WHERE SUBS_SERV_ID = ?
    """
    _max_id = "SELECT max(SUBS_SERV_ID) FROM SUBS_SERVICE"
    _delete_one = 'delete from SUBS_SERVICE WHERE SUBS_SERV_ID = ?;'
    _delete_by_sub_id = 'delete from SUBS_SERVICE WHERE SUBS_ID = ?;'
    del_priority = DeletePriorityConsts.SUBS_SERVICE

    def __init__(self, subs_id, serv_id, serv_stat_id, cre_date=None, subs_serv_id=None,
                 delete_after_test=False) -> None:
        super().__init__(subs_serv_id)
        self.subs_id = subs_id
        self.serv_id = serv_id
        self.serv_stat_id = serv_stat_id
        self.cre_date = cre_date
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=self, priority=self.del_priority)

    @staticmethod
    def get_by_fields_ids(subs_id=None, serv_id=None, serv_stat_id=None,
                          subs_service_table: SubsServiceTable = None,
                          delete_after_test=False) -> SubsServiceTable | None:
        db = SqlServerExecutor()
        if subs_service_table:
            subs_id = subs_service_table.subs_id
            serv_id = subs_service_table.serv_id
            serv_stat_id = subs_service_table.serv_stat_id

        try:
            if subs_id and serv_id and not serv_stat_id:
                t = db.get_data_one(SubsServiceTable.__get_by_subs_and_serv_ids, subs_id, serv_id)
            else:
                t = db.get_data_one(SubsServiceTable.__get_by_ids, subs_id, serv_id, serv_stat_id)
        except ProgrammingError:
            return None
        model = SubsServiceTable.from_tuple(t)
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=model, priority=model.del_priority)
        return model

    @staticmethod
    def from_tuple(tupl) -> SubsServiceTable | None:
        if not tupl:
            return None
        return SubsServiceTable(subs_serv_id=tupl[0],
                                subs_id=tupl[1],
                                serv_id=tupl[2],
                                serv_stat_id=tupl[3],
                                cre_date=tupl[4])

    def ordered(self) -> tuple:
        return self.id, self.subs_id, self.serv_id, self.serv_stat_id, self.cre_date

    def delete_by_sub_id(self, sub_id):
        db = SqlServerExecutor()
        db.modify_data(self._delete_by_sub_id, sub_id)
