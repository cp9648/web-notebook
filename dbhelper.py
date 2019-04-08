# -*- coding: utf-8 -*-
import os
import sqlite3

def judge_sql(sql):
    '''判断sql类型'''
    sql = sql.strip().lower()
    ret = 'fetch'
    if sql.startswith('select'):
        # select
        pass
    elif sql.startswith('update'):
        # update
        ret = 'rowcount'
    elif sql.startswith('delete'):
        # delete
        ret = 'rowcount'
    elif sql.startswith('insert'):
        # insert
        ret = 'rowcount'
    else:
        # create-table, drop-table
        ret = 'table'
    return ret

def db_execute(sql, params=None, fetch_type='one', many=False, db_file=None):
    '''
    执行数据库操作
        sql: SQL语句
        params: SQL语句需要的参数，默认为空（None）
        fetch_type: 当执行查询语句（select）时，获取数据的方法，有以下几种取值情况
            'one': 调用 fetchone()，默认
            'all': 调用 fetchall()
            正整数N: 表示要获取的数据行数，调用 fetchmany(N)
        many: 是否执行 executemany()，默认否，执行 execute()
        db_file: 数据库文件，默认为启动目录下的 'notebook.db'
    '''
    if db_file is None:
        db_file = os.path.join(os.getcwd(), 'notebook.db')
    # 连接数据库
    conn = sqlite3.connect(db_file)
    # 修改查询数据返回格式
    def dict_factory(cursor, row):
        '''修改查询格式'''
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    conn.row_factory = dict_factory
    # 创建游标
    cur = conn.cursor()
    # 执行操作
    if many:
        if params is None:
            params = []
        cur.executemany(sql, params)
    else:
        if params is None:
            params = ()
        cur.execute(sql, params)
    # 判断SQL类型
    sql_type = judge_sql(sql)
    ret = None # 返回值
    if sql_type == 'rowcount':
        # 修改表的语句
        # 返回受影响的行数
        ret = cur.rowcount
        # 提交修改
        conn.commit()
    elif sql_type == 'fetch':
        # 查询数据的语句，需要调用fetch开头的方法，获取数据
        if fetch_type == 'one':
            # 查询一条数据
            ret = cur.fetchone()
        elif fetch_type == 'all':
            # 查询所有数据
            ret = cur.fetchall()
        else:
            # 查询N条数据
            ret = cur.fetchmany(fetch_type)
    else:
        # 创建表的语句，忽略返回值
        pass
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

    return ret

if __name__ == '__main__':
    # 创建tag表
    sql_crete_tag = '''
    CREATE TABLE `tb_tag` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name` TEXT NOT NULL UNIQUE
    )
    '''
    db_execute(sql_crete_tag)
    # 创建note表
    sql_create_note = '''
    CREATE TABLE `tb_note` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `title` TEXT NOT NULL,
        `content` TEXT,
        `tags` TEXT,
        `day` TEXT NOT NULL,
        `pwd` TEXT
    )
    '''
    db_execute(sql_create_note)
