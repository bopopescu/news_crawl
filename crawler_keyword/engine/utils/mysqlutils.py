#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import mysql.connector
from cfg.config import MYSQL_CONFIG

mydb = mysql.connector.connect(
    host=MYSQL_CONFIG["host"],
    port=MYSQL_CONFIG["port"],
    user=MYSQL_CONFIG["user"],
    passwd=MYSQL_CONFIG["passwd"],
    database=MYSQL_CONFIG["database"]
)

def connection_available():
    if not mydb.is_connected():
        return False
    return True


def get_all_stock_ticket():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM stocks")
    results = mycursor.fetchall()
    return [result[0] for result in results]

def get_keywords_by_stock_ticket(stock_ticket:str):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT keywords.name from keywords,stock_keywords where keywords.id = stock_keywords.keywordId and stock_keywords.symbol = '{}'".format(stock_ticket))
    results = mycursor.fetchall()
    return [result[0] for result in results]
def get_symbol():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT symbol FROM stocks")
    results = mycursor.fetchall()
    return [result[0] for result in results]
def get_keywords_by_symbol(symbol:str):
    mycursor = mydb.cursor()
    mycursor.execute("select name from keywords inner join stock_keywords sk on keywords.id = sk.keywordId and sk.symbol = '{}'".format(symbol))
    results = mycursor.fetchall()
    return [results[0] for result in results]

def insert_content_to_mysql(title="", summary="", published="", created="" ,url="" ,image_url="", tokenize_content=""):
    mycursor = mydb.cursor()
    try:
        query = "insert into posts(title,summary,published,created,url,image_url,tokenize_content) values(%s,%s,%s,%s,%s,%s,%s)"
        args = (title, summary, published, created, url, image_url, tokenize_content)
        mycursor.execute(query,args)
        mydb.commit()
        mycursor.reset
    except Exception as e:
        print("Error inserting content to mysql",e)
    return None

def get_postID(url=""):
    mycursor = mydb.cursor()
    query = "select id from posts where url = '{}'".format(url)
    mycursor.execute(query)
    result = mycursor.fetchone()
    result = result[0] if result != None else None
    return result

def insert_post_tags(postId="", content="", symbol="", sentiment=""):
    mycursor = mydb.cursor()
    query = "insert into post_tags(postId,content,symbol,sentiment) values(%s,%s,%s,%s)"
    args = (postId,content,symbol,sentiment)
    mycursor.execute(query,args)
    mydb.commit()
    return None





