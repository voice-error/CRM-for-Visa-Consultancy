import pymysql

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='db_crm',
        cursorclass=pymysql.cursors.DictCursor
    )
