from __future__ import annotations

from framework.utils.datetime_util import DatetimeUtil
from test.constants import DeletePriorityConsts
from test.models.tables.base_table import BaseTable


class TariffTable(BaseTable):
    _get_by_id = """
          SELECT * FROM TARIFF
          WHERE TRPL_ID = ?
      """
    _get_all = """
          SELECT * FROM TARIFF
      """

    _add_one = """
          INSERT INTO
          TARIFF 
          (TRPL_ID, NAME, CRE_DATE, SUMM_INCL)
          VALUES
          (?,?,?,?)"""
    _max_id = "select max(TRPL_ID) from TARIFF;"
    _delete_one = 'delete from TARIFF WHERE TRPL_ID = ?;'

    del_priority = DeletePriorityConsts.TARIFF

    def __init__(self, name, creation_date, price, comment=None, tariff_id=None) -> None:
        super().__init__(tariff_id)
        self.name = name
        self.creation_date = creation_date
        self.price = price
        self.comment = comment

    def ordered(self) -> tuple:
        return self.id, self.name, self.creation_date, self.price, self.comment

    def __eq__(self, other) -> bool:
        return (other.id == self.id
                and other.name.strip() == self.name.strip()
                and DatetimeUtil.datetimes_are_equal_sec_precision(other.creation_date, self.creation_date)
                and other.price == self.price
                and other.comment == self.comment)

    @staticmethod
    def from_tuple(tupl) -> TariffTable:
        return TariffTable(tariff_id=tupl[0],
                           name=tupl[1],
                           creation_date=tupl[2],
                           price=tupl[3],
                           comment=tupl[4])
