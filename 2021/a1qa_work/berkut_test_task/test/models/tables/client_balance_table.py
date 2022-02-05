from __future__ import annotations
from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.logger import Logger
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable
from framework.utils.database_utils.database_cleaner import DatabaseCleaner


class ClientBalanceTable(BaseTable):
    __get_balance_by_client_id = "SELECT * FROM CLIENT_BALANCE WHERE CLNT_ID = ?;"
    _get_by_id = "SELECT * FROM CLIENT_BALANCE WHERE CLNT_BAL_ID = ?"
    __update_balance_summ = """
        UPDATE CLIENT_BALANCE
        SET BALANCE_SUMM = ?
        WHERE CLNT_ID = ?
    """
    _delete_one = "delete from CLIENT_BALANCE where CLNT_BAL_ID = ?"
    _get_balance_summ_by_client_id = "SELECT BALANCE_SUMM FROM CLIENT_BALANCE WHERE CLNT_ID = ?;"
    del_priority = DeletePriorityConsts.CLIENT_BALANCE

    @staticmethod
    def get_balance_summ(clnt_id) -> float:
        db = SqlServerExecutor()
        return db.get_data_one(ClientBalanceTable._get_balance_summ_by_client_id, clnt_id)[0]

    def __init__(self, bal_type_id, clnt_id, bal_stat_id, balance_summ, clnt_bal_id=None, cre_date=None) -> None:
        super().__init__(clnt_bal_id)
        self.bal_type_id = bal_type_id
        self.clnt_id = clnt_id
        self.bal_stat_id = bal_stat_id
        self.cre_date = cre_date
        self.balance_summ = balance_summ

    @staticmethod
    def update_balance_by_id(row_id, balance) -> None:
        db = SqlServerExecutor()
        db.modify_data(ClientBalanceTable.__update_balance_summ, balance, row_id)

    def update_balance_summ(self, balance) -> None:
        Logger.info(f'Изменение баланса клиента с id {self.clnt_id} на сумму {balance}')
        ClientBalanceTable.update_balance_by_id(self.id, balance)
        self.balance_summ = balance

    @staticmethod
    def get_by_client_id(clnt_id, delete_after_test=False) -> ClientBalanceTable:
        db = SqlServerExecutor()
        model = ClientBalanceTable.from_tuple(db.get_data_one(ClientBalanceTable.__get_balance_by_client_id, clnt_id))
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=model, priority=model.del_priority)
        return model

    @staticmethod
    def from_tuple(tupl):
        return ClientBalanceTable(clnt_bal_id=tupl[0],
                                  bal_type_id=tupl[1],
                                  clnt_id=tupl[2],
                                  bal_stat_id=tupl[3],
                                  cre_date=tupl[4],
                                  balance_summ=tupl[5])

    def ordered(self) -> tuple:
        return self.id, self.bal_type_id, self.clnt_id, self.bal_stat_id, self.cre_date, self.balance_summ
