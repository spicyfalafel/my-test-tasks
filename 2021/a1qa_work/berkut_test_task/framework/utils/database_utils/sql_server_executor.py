from framework.singleton import Singleton
from framework.utils.logger import Logger


class SqlServerExecutor(metaclass=Singleton):
    cursor = None

    def set_cursor(self, connection):
        self.cursor = connection.cursor()

    def modify_data(self, query, *args):
        Logger.debug(query)
        Logger.debug(args)
        self.cursor.execute(query, args)
        self.cursor.commit()

    def modify_and_get(self, query, *args):
        Logger.debug(query)
        Logger.debug(args)
        self.cursor.execute(query, args)
        result = self.cursor.fetchval()
        self.cursor.commit()
        return result

    def get_data_one(self, query, *args):
        Logger.debug(query)
        Logger.debug(args)
        self.cursor.execute(query, *args)
        result = self.cursor.fetchone()
        return result

    def get_data_all(self, query, *args):
        Logger.debug(query)
        Logger.debug(args)
        self.cursor.execute(query, *args)
        result = self.cursor.fetchall()
        return result
