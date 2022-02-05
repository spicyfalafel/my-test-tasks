from framework.singleton import Singleton
from framework.utils.logger import Logger
from test.constants import DeletePriorityConsts


class DatabaseCleaner(object, metaclass=Singleton):
    _order = {
        DeletePriorityConsts.TARIFF_SERVICE: [],
        DeletePriorityConsts.SUBS_SERVICE: [],
        DeletePriorityConsts.SERVICE: [],
        DeletePriorityConsts.SUBSCRIBER: [],
        DeletePriorityConsts.TARIFF: [],
        DeletePriorityConsts.CLIENT_BALANCE: [],
        DeletePriorityConsts.CLIENT: [],
        DeletePriorityConsts.SERVICE_ORDERS: []
    }

    def save_to_del_list(self, table, priority=None) -> None:
        if not priority:
            priority = table.del_priority
        self._order[priority].append(table)

    def delete_all_junk(self) -> None:
        deleted = 0
        for order_num, curr_tables in self._order.items():
            for table in curr_tables:
                table.delete()
                deleted += 1
        Logger.info(f'Удалено {deleted} строк из таблиц')
