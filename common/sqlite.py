# coding: utf-8

import sqlite3
import os
import logging

"""
SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说
没有独立的维护进程，所有的维护都来自于程序本身。
在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
数据库文件，而是直接打开该数据库文件。
    连接对象可以是硬盘上面的数据库文件，也可以是建立在内存中的，在内存中的数据库
    执行完任何操作后，都不需要提交事务的(commit)

    创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
    创建在内存上面： conn = sqlite3.connect('"memory:')

    下面我们一硬盘上面创建数据库文件为例来具体说明：
    conn = sqlite3.connect('c:\\test\\hongten.db')
    其中conn对象是数据库链接对象，而对于数据库链接对象来说，具有以下操作：

        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

    cu = conn.cursor()
    这样我们就创建了一个游标对象：cu
    在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
    对于游标对象cu，具有以下具体操作：

        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动
"""
logger = logging.getLogger("bigone")

class ZienSqlite:

    class SqliteError(Exception):
        """
        Base exception for this module.
        """

        pass

    class SqliteAPIError(SqliteError):

        def __init__(self, err_message):
            self.err_message = err_message

        def __str__(self):
            return 'err_message: {:s}'.format(self.err_message)

    def __init__(self, path, verbose=False):
        self.show_sql = verbose if verbose is True else False
        self.conn = None
        self.cur = None
        self.get_conn(path)
        self.get_cursor()

    def get_conn(self, path):
        """
        获取到数据库的连接对象，参数为数据库文件的绝对路径
        如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
        路径下的数据库文件的连接对象；否则，返回内存中的数据接
        连接对象
        :param path:
        :return:
        """

        self.conn = sqlite3.connect(path)
        if os.path.exists(path) and os.path.isfile(path):
            if self.show_sql:
                print('open db:[{}]'.format(path))

        else:
            print("db file not exist.")
            raise self.SqliteAPIError("db file not exist.")

    def get_cursor(self):
        """
        该方法是获取数据库的游标对象，参数为数据库的连接对象
        如果数据库的连接对象不为None，则返回数据库连接对象所创
        建的游标对象；否则返回一个游标对象，该对象是内存中数据
        库连接对象所创建的游标对象
        """
        if self.conn is not None:
            self.cur = self.conn.cursor()
        else:
            print("conn is None.")
            raise self.SqliteAPIError("conn is None.")

    def close_all(self):
        """
        关闭数据库游标对象和数据库连接对象
        """
        try:
            if self.cur is not None:
                self.cur.close()
        finally:
            if self.conn is not None:
                self.conn.close()

    def select(self, sql, data):
        """
        查询一条数据
        :param sql:
        :param data:
        :return:
        """

        if sql is not None and sql != '':
            if data is not None:
                d = (data,)
                if self.show_sql:
                    print('执行sql:[{}],参数:[{}]'.format(sql, data))
                self.cur.execute(sql, d)
                r = self.cur.fetchall()
                return r
            else:
                print('the [{}] equal None!'.format(data))
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def select(self, sql):
        """
        查询一条数据
        :param sql:
        :return:
        """

        if sql is not None and sql != '':

            if self.show_sql:
                print('执行sql:[{}]'.format(sql))
            self.cur.execute(sql)
            r = self.cur.fetchall()
            return r

        else:
            print('the [{}] is empty or equal None!'.format(sql))
