from __future__ import annotations

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.datetime_util import DatetimeUtil
from test.constants import DeletePriorityConsts, DatabasePrecision
from test.models.tables.base_table import BaseTable
from framework.utils.database_utils.database_cleaner import DatabaseCleaner


class ClientTable(BaseTable):
    _max_id = "select max(CLNT_ID) from CLIENT;"

    _create_client = """
    BEGIN
    DECLARE @id int;
    EXECUTE CreateClient	@Name = ?,
                            @ClntTypeId = ?,
                            @BalanceSumm = ?,
                            @ClientId = @id OUTPUT
    SELECT @id
    end"""

    _get_by_id = """
          select * from CLIENT where CLNT_ID = ?;
      """
    _delete_one = "delete from CLIENT WHERE CLNT_ID = ?;"
    del_priority = DeletePriorityConsts.CLIENT

    def create(self, clnt_type_id, balance, delete_after_test=False):
        db = SqlServerExecutor()
        self.id = db.modify_and_get(self._create_client, self.name, clnt_type_id, balance)
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=self, priority=self.del_priority)
        return self.id

    def __init__(self, name, cre_date, client_type_id=None,
                 addr_city=None, addr_street=None, addr_house=None, email=None,
                 comment=None, client_id=None) -> None:
        super().__init__(client_id)
        self.name = name
        self.creation_date = cre_date
        self.client_type_id = client_type_id
        self.addr_city = addr_city
        self.addr_street = addr_street
        self.addr_house = addr_house
        self.email = email
        self.comment = comment

    def __eq__(self, other) -> bool:
        return (other.id == self.id
                and other.client_type_id == self.client_type_id
                and other.name.strip() == self.name.strip()
                and DatetimeUtil.datetimes_are_equal_sec_precision(other.creation_date, self.creation_date,
                                                                   DatabasePrecision.TIME_PRECISION_SEC)
                and self.addr_city == other.addr_city
                and self.addr_house == other.addr_house
                and self.email == other.email
                and self.comment == other.comment)

    @staticmethod
    def from_tuple(tupl) -> ClientTable:
        return ClientTable(client_id=tupl[0],
                           client_type_id=tupl[1],
                           name=tupl[2],
                           cre_date=tupl[3],
                           addr_city=tupl[4],
                           addr_street=tupl[5],
                           addr_house=tupl[6],
                           email=tupl[7],
                           comment=tupl[8])

    def ordered(self) -> tuple:
        return (self.id, self.client_type_id, self.name, self.creation_date,
                self.addr_city, self.addr_street,
                self.addr_house, self.email, self.comment)
