import pymysql
from config import Config

class Mysql(dict):

    def __init__(self, table):
        """
        Args:
            table: table name

        Returns: void
        """
        self.__connect = pymysql.connect(**Config.mysql())
        self.__table = table
        self.__where = ''

        self.__rows = []

    def where(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        where = []
        for column, value in kwargs.items():
            where.append('`%s`="%s"' % (column, str(value)))

        if not self.__where.startswith(' where '):
            self.__where += ' where ' + ' and '.join(where)
        else:
            if len(where) == 1 :
                self.__where += ' and ' +  ''.join(where)
            else:
                self.__where += ' and '.join(where)
        return self

    def where_or(self, **kwargs):
        """

        Args:
            **kwargs:

        Returns:

        """
        where = []
        for column, value in kwargs.items():
            where.append('`%s`="%s"' % (column, str(value)))

        if not self.__where.startswith(' where '):
            self.__where += ' where ' + ' or '.join(where)
        else:
            if len(where) == 1 :
                self.__where += ' or ' +  ''.join(where)
            else:
                self.__where += ' or '.join(where)
        return self


    def find(self):
        """
        Args:
            **kwargs: where
        Returns: sql str
        """
        sql = 'select * from %s' % self.__table
        sql += self.__where
        with self.__connect.cursor() as cursor:
            cursor.execute(sql)
            ret = cursor.fetchone()
            self.__fill_attributes(**ret)
        return self


    def select(self):
        """
        Args:
            **kwargs: where
        Returns: sql str
        """
        sql = 'select * from %s' % self.__table
        sql += self.__where
        print(sql)
        with self.__connect.cursor() as cursor:
            cursor.execute(sql)
            self.__fill_list_attributes(cursor.fetchall())

        return self.__rows


    def __fill_attributes(self, **kwargs):
        """
        填充属性
        Args:
            **kwargs:

        Returns:

        """
        for column, value in kwargs.items():
            self[column] = value


    def __fill_list_attributes(self, rows):
        """
        填充属性
        Args:
            rows:

        Returns:

        """
        for row in rows:
            for column, value in row.items():
                self[column] = value

            self.__rows.append(self)


    def delete(self):
        """
        删除数据
        Returns:

        """
        sql = 'delete from %s' % self.__table
        sql += self.__where
        with self.__connect.cursor() as cursor:
            affected_rows = cursor.execute(sql)
        return affected_rows != 0


    def save(self, **kwargs):
        if kwargs:
            sql = self.__parse_insert_sql(**kwargs)
        else:
            new_dict = {k:v for k,v in self.items() if not k.startswith('_')}
            sql = self.__parse_insert_sql(**new_dict)

        with self.__connect.cursor() as cursor:
            affected_rows = cursor.execute(sql)

        return affected_rows != 0


    def __parse_insert_sql(self, **kwargs):
        """
        解析 insert sql
        Args:
            **kwargs:

        Returns:

        """
        sql = "insert into `%s`" % (self.__table)
        columns = []
        values = []
        for k, v in kwargs.items():
            columns.append('`%s`' % k)
            values.append('"%s"' % v)
        sql += '(%s) values(%s)' % (','.join(columns), ','.join(values))
        return sql


    def __getattr__(self, item):
        return self[item]


    def __setattr__(self, key, value):
        self[key] = value


    def __del__(self):
        self.__connect.close()