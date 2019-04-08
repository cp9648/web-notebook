# -*- coding: utf-8 -*-
import sqlite3
import time
import dbhelper

from datetime import datetime
from flask import (Flask, 
    render_template,
    request,
    session
)


app = Flask(__name__)

app.config['SECRET_KEY'] = '陈鹏的记事本'


@app.route('/edit')
def note_edit():
    '''连接到添加笔记网页'''
    id = request.values.get('id')
    if bool(id):
        sql = '''
        SELECT * from
        tb_note where
        id=?
        '''
        params=(id,)
        data = dbhelper.db_execute(sql, params=params)
        return render_template('edit.html', **data)
    return render_template('edit.html', id=id)


@app.route('/login')
def login():
    '''连接到登录页面'''
    return render_template('login.html')

# ---------------------------------笔记的添加与修改-------------------------------
@app.route('/note_get',methods=['GET','POST'])
def note_get():
    '''内容的添加与修改'''
    # 获取问传递的值
    deit = request.values
    ids = deit.get('id')
    title = deit.get('note-title')
    content = deit.get('note-content')
    tags = deit.get('note-tags')
    date = time.strftime('%Y-%m-%d')
    # 判断值是否为空
    if None in [title, content, tags]:
        return render_template('edit.html')
    # 查询tb_tag中的内容
    if bool(tags):
        # 讲接收的字符串以空格分割并转为小写
        tags_list =[i.lower() for i in tags.split(' ')]
        # 定义sel查询语句
        sql_tag_get = '''
        SELECT * from 
        tb_tag
        '''
        # 查询db_tag表中的所以数据
        data = dbhelper.db_execute(sql_tag_get, fetch_type='all')
        # 判断数据库中存不存在输入的标签并返回一个列表
        j = [i for i in tags_list if i not in [i['name'] for i in data]]
        # 将不存在的标签添加到列表中
        sql_tag_sel = '''
        INSERT INTO TB_TAG(name)
        VALUES(?)
        '''
        # 执行循环添加不存在的标签
        for i in j:
            data = dbhelper.db_execute(sql=sql_tag_sel, params=(i,))
            if data:
                print('ok')
    # 创建sql添加语句
    sql = '''
    INSERT INTO TB_NOTE(title, content, tags, day)
    VALUES(?, ?, ?, ?)
    '''
    stu = (title, content, tags, date)
    
    # 创建sql修改语句
    sql_up = '''    
    UPDATE TB_NOTE SET 
        title=?,
        content=?,
        tags=?
    where id=?
    '''
    stu_up = (title, content, tags, ids)
    # 判断ids是否存在（执行添加还是修改）
    if bool(ids):
        data = dbhelper.db_execute(sql=sql_up, params=stu_up)  # 修改
    else:
        data = dbhelper.db_execute(sql=sql, params=stu)  # 添加
    # 接收返回的结构
    if int(data) == 1:
        return note_list()
    return '为什么出错呢？你想想吧'


# ------------------------------------- 登录 ----------------------------------
@app.route('/user', methods=['GET','POST'])
def user():
    '''登录判断'''
    deit = request.values
    name = deit.get('name')
    pwd = deit.get('pwd')
    sql = '''
    SELECT * from tb_user
    where name=? 
    and pwd=?
    '''
    stu =(name, pwd)
    data = dbhelper.db_execute(sql, params=stu)
    if data:
        session['name'] = name
        session['pwd'] = pwd
        return note_list()
    return str('你自己的账号和密码都记不住吗？')


# ----------------------------------- 笔记内容查看页面 ------------------------------
@app.route('/details/<id>')
def details(id=None):
    '''详细信息展示页面'''
    sql = '''
    SELECT * from tb_note
    where id=?
    '''
    params=(int(id),)
    data = dbhelper.db_execute(sql, params=params)
    return render_template('details.html', **data)


# ------------------------------------ 主页面 ---------------------------------------
@app.route('/')
def note_list():
    # 查询tb_note数据库
    sql = '''
    SELECT * from 
    tb_note
    '''
    result = dbhelper.db_execute(sql=sql, fetch_type='all')
    # 查询tb_tag数据库
    sql_tag = '''
    SELECT * from 
    tb_tag
    '''
    tags = {}
    result_tag = dbhelper.db_execute(sql=sql_tag, fetch_type='all')
    tag_list = [i['name'] for i in result_tag]
    tag_list.insert(0, '全部')
    for idx, item in enumerate(tag_list):
        tags[str(idx)] = item
    results = []
    req_tag = request.values.get('hid-tags', '')
    req_query = request.values.get('query', '')
    req_day = request.values.get('req_day', '')
    if bool(req_day):
        sql_day = '''
        SELECT * from 
        tb_note where 
        day=?
        '''
        params=(req_day,)
        result = dbhelper.db_execute(sql=sql_day, params=params, fetch_type='all')
    if bool(req_query):
        sql_query = '''
        SELECT * from 
        tb_note where 
        title like '%{0}%'
        '''.format(req_query)
        result = dbhelper.db_execute(sql=sql_query, fetch_type='all')
    selected = req_tag.split(',')
    if bool(req_tag):
        # 循环已经选中标签
        for s in selected:
            # 查出选择的项的名称
            req_tag_name =''.join([i['name'] for i in result_tag if i['id'] == int(s)])
            for i in result:
                if req_tag_name in i['tags'].split(' ') and i not in results:
                    results.append(i)
    else:
        results.extend(result)
    if '0' in selected:
        selected = ['0']
    # 获取数据库‘day’属性并去重复
    days = {i['day']:None for i in result}
    max_day = datetime.now().day + 1
    # 获取页面的
    if bool(results):
        results=result
    params = {
        'tags': tags,
        'selected': selected,
        'days': ['2018-08-{0:02d}'.format(i) for i in range(1, max_day)],
        'result': results
    }
    return render_template('index.html', **params)


# 删除
@app.route('/deletes')
def deletes():

    id = request.values.get('id')
    sql = '''
    DELETE from tb_note
    where id=?
    '''
    params=(id,)
    data = dbhelper.db_execute(sql, params=params)
    print(data)
    if data:
        return note_list()
    return '糟了,这是怎么回事？'


if __name__ == '__main__':
    cfg = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True
    }
    app.run(**cfg)
