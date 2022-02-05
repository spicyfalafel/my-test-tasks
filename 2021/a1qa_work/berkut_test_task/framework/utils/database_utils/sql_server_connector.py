import pyodbc

from framework.singleton import Singleton
from framework.utils.logger import Logger


class SqlServerConnector(metaclass=Singleton):

    def connect(self, host, database, username, password, port):
        server_part = f';SERVER={host}' if host else ''
        database_part = f';DATABASE={database}' if database else ''
        user_part = f';USER={username}' if username else ''
        password_part = f';PASSWORD={password}' if password else ''
        port_part = f';PORT={port}' if port else ''
        connection_arg = f'DRIVER={{SQL Server}}{server_part}{database_part}{user_part}{password_part}{port_part}'
        Logger.info(f'Соединение с базой данных: {connection_arg}')
        conn = pyodbc.connect(connection_arg)
        return conn
