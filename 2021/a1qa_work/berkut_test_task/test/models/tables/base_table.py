from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, TypeVar

from framework.utils.database_utils.sql_server_executor import SqlServerExecutor
from framework.utils.database_utils.database_cleaner import DatabaseCleaner

T = TypeVar('T', bound='TrivialClass')


class BaseTable(ABC):
    _add_one: str
    _max_id: str
    _get_all: str
    _get_by_id: str
    _delete_one: str
    _delete_all: str
    del_priority: int

    def __init__(self, row_id):
        if row_id:
            self.id = row_id
        else:
            max_id = self.get_max_id()
            self.id = max_id + 1 if max_id else 1

    def get_max_id(self) -> int:
        db = SqlServerExecutor()
        return db.get_data_one(self._max_id)[0]

    @classmethod
    def get_by_id(cls: Type[T], row_id: int) -> T:
        db = SqlServerExecutor()
        t = db.get_data_one(cls._get_by_id, row_id)
        return cls.from_tuple(t)

    def refresh(self):
        return self.get_by_id(self.id)

    def __str__(self) -> str:
        return f" (id={self.id})" + super().__str__()

    @classmethod
    def get(cls: Type[T]) -> T:
        db = SqlServerExecutor()
        data_tuples = db.get_data_all(cls._get_all)
        return tuple(cls.from_tuple(t) for t in data_tuples)

    def _ordered(self) -> tuple:
        tupl = self.ordered()
        return tuple(el for el in tupl if el)

    def add_to_db(self, delete_after_test=False):
        db = SqlServerExecutor()
        max_id = db.get_data_one(self._max_id)[0]
        self.id = max_id + 1
        db.modify_data(self._add_one,
                       *self._ordered())
        if delete_after_test:
            DatabaseCleaner().save_to_del_list(table=self)
        return self.id

    def delete(self) -> None:
        db = SqlServerExecutor()
        db.modify_data(self._delete_one, self.id)

    @classmethod
    def delete_all(cls) -> None:
        db = SqlServerExecutor()
        db.modify_data(cls._delete_all)

    @staticmethod
    @abstractmethod
    def from_tuple(tupl) -> T:
        pass

    @abstractmethod
    def ordered(self) -> tuple:
        pass
