import csv
import time
import pymysql
from flask import jsonify, request

from apps.models.blog_model import weather
from exts import db


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")

def get_conn():
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='wwa',
                           passwd='000159wwa',
                           db='mydb1',
                           charset='utf8')
    cursor = conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    cursor.close()
    conn.close()

def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res
def get_1():
    sql = 'select time,average from ave_data'
    res = query(sql)
    return res

def delete(str0):
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
        sql = 'delete from ' + str0 + ' where 1 = 1'
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

#第一个变量是数据库名，第二个变量是城市名，变量一定要加单引号''
def change_data(str0):
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
        sql = 'delete from ' + str0 + ' where 1 = 1'
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
    average_file = u'C:\\Users\\90952\\PycharmProjects\\blog\\weather\\' + t1 + '_result.csv'
    csv_file = open(average_file)  # 打开csv文件
    csv_reader_lines = csv.reader(csv_file)  # 逐行读取csv文件
    date = []  # 创建列表准备接收csv各行数据

    row = 0
    for one_line in csv_reader_lines:
        date.append(one_line)  # 将读取的csv分行数据按行存入列表‘date’中
        # print(date[row][0])
        # print(date[row][1])
        # print(date[row][2])
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
            print(row)
            print(data.time)
            print(data.max)
            print(data.min)
            print(data.ave)

            # # 3.向数据库提交数据
            db.session.add(data)
            db.session.commit()
        row = row + 1  # 统计行数（这里是学生人数）




def select(t1, t2):
    sql = 'select '+t1+' from '+t2
    res = query(sql)
    return res


if __name__ == "__main__":
    change_data('weather')

