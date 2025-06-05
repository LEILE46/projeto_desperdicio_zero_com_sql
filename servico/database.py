import pymysql
from pymysql.cursors import DictCursor  

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="doacao_alimentos",
        cursorclass=DictCursor 
    )