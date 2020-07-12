import csv
import hashlib
import json
import string

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from numpy.ma import var
import pymysql

from apps.models.blog_model import User, Data, Ave_data, 全国, weather, weather_real, weather_con, 人员管理
from exts import db
from test import query, get_time, delete, select, get_conn, close_conn
from test.pachong import crawler, crawler2
b=['北京','天津','河北','山西','内蒙古','黑龙江','吉林','辽宁','上海','安徽','江苏','山东','浙江','福建','江西','湖北','湖南','河南','广西','广东','海南','陕西','甘肃','新疆','青海','宁夏','四川','重庆','贵州','云南','西藏']
blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

testInfo = {}
num = 10
x = [{ 'name': '北京' , 'value':100000}]

@blog_bp.route('/jingli', methods=['GET','POST'])
def jingli():
    l = []
    department = findd(session["username"])
    sql = "select username,position,department from 人员管理 where department = '"+department[0][0]+"' and position != 'ceo'"
    res = query(sql)

    for a, b, c in res:
        # time.append(a.strftime("%m-%d"))
        list = {}
        list["姓名"] = a
        list["职务"] = b
        list["部门"] = c
        l.append(list)
        # print(list)

        # print(l)
    print(l)

    return jsonify(l)

@blog_bp.route('/try3', methods=['GET','POST'])
def try13():
    l = []
    sql = 'select username,position,department from 人员管理'
    res = query(sql)

    for a, b, c in res:
        # time.append(a.strftime("%m-%d"))
        list = {}
        list["姓名"] = a
        list["职务"] = b
        list["部门"] = c
        l.append(list)
        # print(list)

        # print(l)
    print(l)

    return jsonify(l)

@blog_bp.route('/guanli',endpoint='guanli')
def guanli():
    res = findp(session["username"])
    #res[0][0]是所求值
    position = res[0][0]
    if position == '员工':
        return render_template('yuangong.html')
    elif position == '经理':
        return render_template('jingli1.html')
    elif position == 'ceo':
        return render_template('ceo1.html')


@blog_bp.route('/logout',endpoint='logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('blog.map'))

@blog_bp.route('/map', endpoint='map')
def upload():
    print(session)
    return render_template('test3.html')

@blog_bp.route('/', endpoint="sy")
def upload111():
    return render_template('a.html')

def insert(t1,t2,t3,t4):
    sql = "insert into 人员管理(username,password,position,department) values('" + t1 + "','" + t2 + "','" + t3 + "','" + t4 + "')"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)

@blog_bp.route('/insert_y', endpoint='insert_y', methods=['GET','POST'])
def insert_p1():
    username = request.form.get('username')
    user = 人员管理.query.filter_by(username=username).first()
    if not user :
        password = request.form.get('password')
        department = findd(session["username"])[0][0]
        insert(username, password, '员工', department)
        return render_template('jingli3.html')
    else:
        return render_template('jingli3.html',msg ='已存在该用户')

@blog_bp.route('/insert_j', endpoint='insert_j', methods=['GET','POST'])
def insert_p():
    username = request.form.get('username')
    user = 人员管理.query.filter_by(username=username).first()
    if not user:
        password= request.form.get('password')
        department = request.form.get('department')
        insert(username,password,'经理',department)
        return render_template('ceo4.html')
    else:
        return render_template('ceo4.html',msg ='已存在该用户')

def layoffs(username):
    sql = "delete from 人员管理 where username ='"+username+"'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)

def replace(username, de, new):
    sql = "update 人员管理 set "+de+" = '"+new+"' where username = '"+username+"'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)

@blog_bp.route('/replace', endpoint='replace', methods=['GET','POST'])
def replaceddd():
    username = request.form.get('name')
    position = request.form.get('position')
    user = 人员管理.query.filter_by(username=username).first()
    if not user:
        return render_template('ceo2.html',msg = '请输入正确的姓名')
    elif position == '经理' or position == '员工':
        replace(username,'position', position)
        return render_template('ceo2.html')
    else:
        return render_template('ceo2.html',msg1 = '职务只能选择经理或者员工')

@blog_bp.route('/replace1', endpoint='replace1', methods=['GET','POST'])
def replaceddd1():
    username = request.form.get('name')
    department = request.form.get('department')

    user = 人员管理.query.filter_by(username=username).first()
    if not user:
        return render_template('ceo3.html', msg='请输入正确的姓名')
    else:
        position = findp(username)[0][0]
        if position == '员工':
            replace(username,'department', department)
            replace(username, 'position', '经理')
            return render_template('ceo3.html')
        else:
            return render_template('ceo3.html',msg = '请选择员工')

def delete_depart(department):
    sql = "delete from 人员管理 where department = '"+department+"'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)

@blog_bp.route('/deletedepart', endpoint='delete_depart', methods=['GET','POST'])
def delete_departddd():
    department = request.form.get('department')
    de = 人员管理.query.filter_by(department=department).first()
    if department == '0':
        return render_template('ceo1.html',msg = '不能删除部门0')
    elif not de:
        return render_template('ceo1.html',msg = '不存在该部门')
    else:
        delete_depart(department)
        return render_template('ceo1.html')

def delete_departy(username):
    sql = "delete from 人员管理 where username = '"+username+"'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    close_conn(conn, cursor)

@blog_bp.route('/deletey', endpoint='delete_y', methods=['GET','POST'])
def delete_dy():
    de = findd(session["username"])[0][0]
    department = request.form.get('username')
    user = 人员管理.query.filter_by(username=department,department=de).first()
    if not user:
        return render_template('jingli1.html', msg='请输入本部门员工的姓名')
    else:
        y = findp(department)[0][0]
        if y == '员工':
            delete_departy(department)
            return render_template('jingli1.html')
        else:
            return render_template('jingli1.html',msg='请输入本部门员工的姓名')

def find(de,value):
    sql = "select * from 人员管理 where "+de+" = '" + value + "'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def findp(value):
    sql = "select position from 人员管理 where username = '" + value + "'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def findd(value):
    sql = "select department from 人员管理 where username = '" + value + "'"
    conn, cursor = get_conn()
    cursor.execute(sql)
    conn.commit()
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

@blog_bp.route('/insert')
def table():
    insert('经理','123','经理','1')
    # layoffs('王伟安')
    # replace('王伟安', 'position', 'boss')
    # res = find('position','员工')
    return 'jsonify(res)'

@blog_bp.route('/table')
def table1():
    sql = 'select username,password,position,department from 用户管理;'
    res = query(sql)
    username, password, position, department = [], [], [], []
    for a, b, c, d in res:
        # time.append(a.strftime("%m-%d"))
        username.append(a)
        password.append(b)
        position.append(c)
        department.append(d)
    data = jsonify({"username": username, "password": password, "position": position, "department": department})
    return data


@blog_bp.route('/l2', methods=['GET','POST'])
def test12():
    if request.method == 'POST':
        a = request.get_data("city")
        b = a.decode()
        print(b)
        change(b)
        change1(b)
        change2(b)

    sql = 'select time,max,min,ave from weather'
    res = query(sql)
    # #res[第几个元组][元组的第几个数据]
    # return res[3][0]+ " , "+res[3][1]
    time, max, min, ave= [],[],[],[]
    for a,b,c,d in res:
        # time.append(a.strftime("%m-%d"))
        time.append(a)
        max.append(b)
        min.append(c)
        ave.append(d)

    sql = 'select time,max,min,ave from weather_real'
    res = query(sql)
    # #res[第几个元组][元组的第几个数据]
    # return res[3][0]+ " , "+res[3][1]
    timer, maxr, minr, aver = [], [], [], []
    for a, b, c, d in res:
        # time.append(a.strftime("%m-%d"))
        timer.append(a)
        maxr.append(b)
        minr.append(c)
        aver.append(d)

    sql = 'select time,max,min,ave from weather_con'
    res = query(sql)
    # #res[第几个元组][元组的第几个数据]
    # return res[3][0]+ " , "+res[3][1]
    timec, maxc, minc, avec = [], [], [], []
    for a, b, c, d in res:
        # time.append(a.strftime("%m-%d"))
        timec.append(a)
        maxc.append(b)
        minc.append(c)
        avec.append(d)

    data = jsonify({"time":time,"min":min,"max":max,"ave":ave,"timer":timer,"minr":minr,"maxr":maxr,"aver":aver,"timec":timec,"minc":minc,"maxc":maxc,"avec":avec})
    # print(data)
    # print(type(data))
    # print(type(data))
    # print(type(data))
    # print(type(data))
    return data

@blog_bp.route('/l1', methods=['GET','POST'])
def test11():
    sql = 'select time,average from ave_data'
    res = query(sql)
    day, average= [],[]
    for a,b in res:
        # time.append(a.strftime("%m-%d"))
        day.append(a)
        average.append(b)


        data = jsonify({"day":day,"average":average})
    print(data)
    print(type(data))
    print(type(data))
    print(type(data))
    print(type(data))
    return render_template('try.html', data =day)







@blog_bp.route('/main', methods=['GET','POST'])
def main():
    return render_template('main.html')


@blog_bp.route('/test', methods=['GET','POST'])
def time():
    return render_template('test.html')



@blog_bp.route('/sendjson', methods=['GET','POST'])
def sendjson():


  # 接受前端发来的数据
  data = json.loads(request.form.get('data'))

  # lesson: "Operation System"
  # score: 100
  lesson = data["lesson"]
  score = data["score"]
  # 自己在本地组装成Json格式,用到了flask的jsonify方法
  info = dict()
  info['name'] = "pengshuang"
  info['lesson'] = lesson
  info['score'] = score
  return jsonify(info)

@blog_bp.route('/taichou', endpoint='index')
def index():
    json_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\min.json'
    with open(json_file, 'r') as load_f:
        load_dict = json.load(load_f)
        print(type(load_dict))
        jo = json.dumps(load_dict)
        print(type(jo))




    return render_template('index.html', load = load_dict)

@blog_bp.route('/login', endpoint='login', methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        username = request.form.get('username')
        p1 = request.form.get('password1')
        pwd = p1

        user = 人员管理.query.filter_by(username=username).first()
        if not user:
            return render_template('login.html', msg='用户不存在')
        else:
            if pwd != user.password:
                return render_template('login.html', msg='密码错误')
            else:
                session["username"] = username
                return redirect(url_for('blog.map'))


    user = User.query.get(1)
    print(user.password)
    return render_template('login.html')


@blog_bp.route('/register', endpoint='register', methods=['GET','POST'])
def user_register():
    if request.method=='POST':
        username = request.form.get('username')
        p1 = request.form.get('password1')
        p2 = request.form.get('password2')
        user = User.query.filter_by(username=username).first()
        if not user:
            if p1==p2:
                #存放到数据库
                pwd = p1
                print(pwd)
                #添加数据步骤：
                #1.先创建模型对象
                user = 人员管理()
                #2.给对象赋值
                user.username = username
                user.password = pwd
                user.position = '员工'
                user.department = '1'
                #3.向数据库提交数据
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('blog.map'))
            else:
                return render_template('register.html', msg='密码不一致')
        else:
            return render_template('register.html', msg='用户名已被注册')
    return render_template('register.html')


def change2(t2):
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'wwa',
        'passwd': '000159wwa',
        'db': 'mydb1',
        'charset': 'utf8'
    }
    # 打开数据库连接
    conn = pymysql.connect(**config)
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        print("0")
        # SQL 删除语句
        sql = 'delete from weather_con where 1 = 1'
        print("1")
        # 执行SQL语句
        cursor.execute(sql)
        print("2")
        # 确认修改
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭链接
        conn.close()
        print("删除成功")
    except:
        print("删除失败")
    average_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\' + t2 + '_con.csv'
    csv_file = open(average_file)  # 打开csv文件
    csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
    date = []  # 创建列表准备接收csv各行数据

    row = 0
    for one_line in csv_reader_lines:
        date.append(one_line)  # 将读取的csv分行数据按行存入列表‘date’中
        if row != 0:
            # # 1.先创建模型对象
            # user = User()
            data = weather_con()
            # # 2.给对象赋值
            # user.username = username
            # user.password = pwd
            data.time = date[row][0]
            data.max = str(date[row][1])
            data.min = str(date[row][2])
            data.ave = str(date[row][3])
            # # 3.向数据库提交数据
            db.session.add(data)
            db.session.commit()
        row = row + 1  # 统计行数（这里是学生人数）

def change1(t2):
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'wwa',
        'passwd': '000159wwa',
        'db': 'mydb1',
        'charset': 'utf8'
    }
    # 打开数据库连接
    conn = pymysql.connect(**config)
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        print("0")
        # SQL 删除语句
        sql = 'delete from weather_real where 1 = 1'
        print("1")
        # 执行SQL语句
        cursor.execute(sql)
        print("2")
        # 确认修改
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭链接
        conn.close()
        print("删除成功")
    except:
        print("删除失败")
    average_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\' + t2 + '_real.csv'
    csv_file = open(average_file)  # 打开csv文件
    csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
    date = []  # 创建列表准备接收csv各行数据

    row = 0
    for one_line in csv_reader_lines:
        date.append(one_line)  # 将读取的csv分行数据按行存入列表‘date’中
        if row != 0:
            # # 1.先创建模型对象
            # user = User()
            data = weather_real()
            # # 2.给对象赋值
            # user.username = username
            # user.password = pwd
            data.time = date[row][0]
            data.max = str(date[row][1])
            data.min = str(date[row][2])
            data.ave = str(date[row][3])
            # # 3.向数据库提交数据
            db.session.add(data)
            db.session.commit()
        row = row + 1  # 统计行数（这里是学生人数）

def change(t2):
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'wwa',
        'passwd': '000159wwa',
        'db': 'mydb1',
        'charset': 'utf8'
    }
    # 打开数据库连接
    conn = pymysql.connect(**config)
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        print("0")
        # SQL 删除语句
        sql = 'delete from weather where 1 = 1'
        print("1")
        # 执行SQL语句
        cursor.execute(sql)
        print("2")
        # 确认修改
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭链接
        conn.close()
        print("删除成功")
    except:
        print("删除失败")
    average_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\' + t2 + '_result.csv'
    csv_file = open(average_file)  # 打开csv文件
    csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
    date = []  # 创建列表准备接收csv各行数据

    row = 0
    for one_line in csv_reader_lines:
        date.append(one_line)  # 将读取的csv分行数据按行存入列表‘date’中
        if row != 0:
            # # 1.先创建模型对象
            # user = User()
            data = weather()
            # # 2.给对象赋值
            # user.username = username
            # user.password = pwd
            data.time = date[row][0]
            data.max = str(date[row][1])
            data.min = str(date[row][2])
            data.ave = str(date[row][3])
            # # 3.向数据库提交数据
            db.session.add(data)
            db.session.commit()
        row = row + 1  # 统计行数（这里是学生人数）

@blog_bp.route('/try2', methods=['GET','POST'])
def try12():
    row = 0
    a = crawler2()
    print(type(a))
    for c in a:
        # print(c['name'][0])
        # print(c['name'])
        a[row]['name'] = b[row]
        a[row]['value'] = c['value'][0]
        row += 1
    print(a)

    return jsonify(a)

@blog_bp.route('/try', methods=['GET','POST'])
def try11():
    row = 0
    a = crawler()
    print(type(a))
    for c in a:
        # print(c['name'][0])
        # print(c['name'])
        a[row]['name'] = b[row]
        a[row]['value'] = c['value'][0]
        row += 1
    print(a)

    return jsonify(a)


@blog_bp.route('/load_china')
def upload11():
    delete(全国)
    a = crawler()
    print(type(a))
    for b in a:
        # # 1.先创建模型对象
        # user = User()
        data = 全国()
        # # 2.给对象赋值
        # user.username = username
        # user.password = pwd
        data.time = b['name'][0]
        data.data = b['value'][0]
        # # 3.向数据库提交数据
        db.session.add(data)
        db.session.commit()
    return 'jsonify(a)'



@blog_bp.route('/time', methods=['GET','POST'])
def gettime():
    return get_time()


@blog_bp.route('/load_csv', methods=['GET','POST'])
def test1():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'wwa',
        'passwd': '000159wwa',
        'db': 'mydb1',
        'charset': 'utf8'
    }
    # 打开数据库连接
    conn = pymysql.connect(**config)
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        print("0")
        # SQL 删除语句
        sql = 'delete from Ave_data where 1 = 1'
        print("1")
        # 执行SQL语句
        cursor.execute(sql)
        print("2")
        # 确认修改
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭链接
        conn.close()
        print("删除成功")
    except:
        print("删除失败")
    t1 = '北京'
    average_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\'+t1+'average_result.csv'
    csv_file = open(average_file)  # 打开csv文件
    csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
    date = []  # 创建列表准备接收csv各行数据

    row = 0
    for one_line in csv_reader_lines:
        date.append(one_line)  # 将读取的csv分行数据按行存入列表‘date’中
        print(date[row][0])
        print(date[row][1])
        print(date[row][2])
        if row != 0:
        # # 1.先创建模型对象
        # user = User()
            data = weather()
        # # 2.给对象赋值
        # user.username = username
        # user.password = pwd
            data.time = date[row][0]
            data.max = str(date[row][1])
            data.min = str(date[row][2])
            data.ave = str(date[row][3])
        # # 3.向数据库提交数据
            db.session.add(data)
            db.session.commit()
        row = row + 1  # 统计行数（这里是学生人数）
    return 'POST'

@blog_bp.route('/load_json', methods=['GET','POST'])
def test():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'wwa',
        'passwd': '000159wwa',
        'db': 'mydb1',
        'charset': 'utf8'
    }
    # 打开数据库连接
    conn = pymysql.connect(**config)
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = conn.cursor()
        print("0")
        # SQL 删除语句
        sql = 'delete from data where 1 = 1'
        print("1")
        # 执行SQL语句
        cursor.execute(sql)
        print("2")
        # 确认修改
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭链接
        conn.close()
        print("删除成功")
    except:
        print("删除失败")

    json_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\min.json'
    with open(json_file, 'r') as load_f:
        load_dict = json.load(load_f)
        print(type(load_dict))
        print(load_dict.items())
        id = 0
        for k in load_dict:
            print(k + "," + str(load_dict[k]))
            id += 1
        # # 1.先创建模型对象
        # user = User()
            data = Data()
        # # 2.给对象赋值
        # user.username = username
        # user.password = pwd
            data.id =  id
            data.time = k
            data.tmin = str(load_dict[k])
        # # 3.向数据库提交数据
            db.session.add(data)
            db.session.commit()

    return load_dict


@blog_bp.route('/ceo1',endpoint='ceo1')
def ceo1():
    b = findp(session["username"])[0][0]
    if b == 'ceo':
        return render_template('ceo1.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/ceo2',endpoint='ceo2')
def ceo2():
    b = findp(session["username"])[0][0]
    if b == 'ceo':
        return render_template('ceo2.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/ceo3',endpoint='ceo3')
def ceo3():
    b = findp(session["username"])[0][0]
    if b == 'ceo':
        return render_template('ceo3.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/ceo4',endpoint='ceo4')
def ceo4():
    b = findp(session["username"])[0][0]
    if b == 'ceo':
        return render_template('ceo4.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/jingli1',endpoint='jingli1')
def jingli1():
    b = findp(session["username"])[0][0]
    if b == '经理':
        return render_template('jingli1.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/jingli2',endpoint='jingli2')
def jingli2():
    b = findp(session["username"])[0][0]
    if b == '经理':
        return render_template('jingli2.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/jingli3',endpoint='jingli3')
def jingli3():
    b = findp(session["username"])[0][0]
    if b == '经理':
        return render_template('jingli3.html')
    else:
        return render_template('test3.html')

@blog_bp.route('/jingli4',endpoint='jingli4')
def jingli4():
    b = findp(session["username"])[0][0]
    if b == '经理':
        return render_template('jingli4.html')
    else:
        return render_template('test3.html')