from pymysql import *

conn = connect(host='localhost', user='root', passwd='root', database='steamdata', port=3306, charset='utf8mb4')

cursor = conn.cursor()


def querys(sql, params, type='no_select'):
    params = tuple(params)
    cursor.execute(sql, params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return 'SQL params executed successfully'
