import mysql.connector
from cfg.config import MYSQL_CONFIG

def connect():
    mydb = mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        user=MYSQL_CONFIG["user"],
        passwd=MYSQL_CONFIG["passwd"],
        database=MYSQL_CONFIG["database"]
    )
    mycursor = mydb.cursor()
    print("connected")