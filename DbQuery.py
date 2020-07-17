# -*- coding: utf-8 -*-
"""
:authors: MaksimFokht
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2020 MaksimFokht
"""

import psycopg2
import bot_config


class Query:
    """

    :param query: Строка запроса в БД.
    :type query: str

    Данный класс служит для соединения с БД PostgreSQL.
    """

    def __init__(self, query):
        self.query = query

    def db_query_nrt(self):  # no return data (НЕ ТРОГАТЬ)
        """
        Метод, выполняющий запрос пользователя к БД. Не имеет возвращаемых данных.
        """
        conn_nrt = None
        try:
            conn_nrt = psycopg2.connect(bot_config.DATABASE_URL, sslmode='require')
            comm = conn_nrt.cursor()
            comm.execute(self.query)
            print('[DEBUG-NRT]: Success')
        except (Exception, psycopg2.Error) as error:
            print('[DEBUG-NRT]: An exception occurred - ', error)
        finally:
            if conn_nrt:
                conn_nrt.commit()
                conn_nrt.close()
                print('[DEBUG-NRT]: DB Connection is closed')

    def db_query_wrt(self):  # with return data (НЕ ТРОГАТЬ)
        """
        Метод, выполняющий запрос пользователя к БД. Имеет возвращаемые данные.

        :return: data: Возвращает словарь из массивов данных из БД.
        """
        conn_wrt = None
        try:
            conn_wrt = psycopg2.connect(bot_config.DATABASE_URL, sslmode='require')
            comm = conn_wrt.cursor()
            comm.execute(self.query)
            data = comm.fetchall()
            print('[DEBUG-WRT]: Success')
            return data
        except (Exception, psycopg2.Error) as error:
            print('[DEBUG-WRT]: An exception occurred - ', error)
        finally:
            if conn_wrt:
                conn_wrt.commit()
                conn_wrt.close()
                print('[DEBUG-WRT]: DB Connection is closed')
