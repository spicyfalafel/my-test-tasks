from __future__ import annotations

from pyodbc import ProgrammingError

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable
from framework.utils.database_utils.database_cleaner import DatabaseCleaner


class SubscriberTable(BaseTable):
    _max_id = "select max(SUBS_ID) from SUBSCRIBER;"
    _get_by_id = """
          SELECT * FROM SUBSCRIBER  
          WHERE SUBS_ID = ?
      """
    _get_all = """
          SELECT * FROM SUBSCRIBER
      """
    _delete_one = "delete from SUBSCRIBER WHERE SUBS_ID = ?"
    __create_subscriber = """
    BEGIN
    DECLARE @id int;
    EXECUTE CreateSubscriber	@Name = ?,							
                                @ClientId = ?,
                                @TrplId=?,
                                @Msisdn = ?,
                                @SubscriberId = @id OUTPUT
    SELECT @id
    end"""

    __activate_subscriber = """
    BEGIN
    DECLARE @errmsg nchar(100);
    EXECUTE ActivateSubscriber	
        @SubsId = ?,
        @ErrMsg = @errmsg OUTPUT;
        SELECT @errmsg;
    end
    """

    del_priority = DeletePriorityConsts.SUBSCRIBER

    # CreateSubscriber procedure
    def create(self, delete_after_test=False):
        db = SqlServerExecutor()
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=self, priority=self.del_priority)
        self.id = db.modify_and_get(self.__create_subscriber, self.name, self.clnt_id, self.trpl_id, self.msisdn)
        return self.id

    # ActivateSubscriber
    def activate(self):
        try:
            db = SqlServerExecutor()
            db.modify_data(self.__activate_subscriber, self.id)
        except ProgrammingError as e:
            return str(e)

    def __init__(self, name, clnt_id, trpl_id, cre_date, comment=None, msisdn=None, subs_stat_id=None,
                 subs_id=None) -> None:
        super().__init__(subs_id)
        self.name = name
        self.subs_stat_id = subs_stat_id
        self.clnt_id = clnt_id
        self.msisdn = msisdn
        self.trpl_id = trpl_id
        self.comment = comment
        self.creation_date = cre_date

    def ordered(self) -> tuple:
        return (self.id, self.name, self.subs_stat_id, self.clnt_id, self.msisdn,
                self.trpl_id, self.comment, self.creation_date)

    @staticmethod
    def from_tuple(tupl):
        return SubscriberTable(subs_id=tupl[0], name=tupl[1], subs_stat_id=tupl[2],
                               clnt_id=tupl[3], msisdn=tupl[4], trpl_id=tupl[5],
                               comment=tupl[6], cre_date=tupl[7])
