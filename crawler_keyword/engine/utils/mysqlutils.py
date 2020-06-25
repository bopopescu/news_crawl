import mysql.connector
from cfg.config import MYSQL_CONFIG

mydb = mysql.connector.connect(
    host=MYSQL_CONFIG["host"],
    user=MYSQL_CONFIG["user"],
    passwd=MYSQL_CONFIG["passwd"],
    database=MYSQL_CONFIG["database"]
)
mycursor = mydb.cursor()

def connection_available():
    if not mydb.is_connected():
        return False
    return True


def get_all_stock_ticket():
    mycursor.execute("SELECT * FROM stock")
    results = mycursor.fetchall()
    return [result[0] for result in results]

def get_keywords_by_stock_ticket(stock_ticket:str):
    mycursor.execute("SELECT keyword.keyWord from keyword,crawlkey where crawlkey.keywordId = keyword.keywordId and crawlkey.stockTicket = '{}'".format(stock_ticket))
    results = mycursor.fetchall()
    return [result[0] for result in results]
def get_symbol():
    mycursor.execute("SELECT symbol FROM stocks")
    results = mycursor.fetchall()
    return [result[0] for result in results]
def get_keywords_by_symbol(symbol:str):
    mycursor.execute("select name from keywords inner join stock_keywords sk on keywords.id = sk.keywordId and sk.symbol = '{}'".format(symbol))
    results = mycursor.fetchall()
    return [results[0] for result in results]

def insert_content_to_mysql(content, published, created, url, tokenize_content, sentiment):
    query = "insert into post(content,published,created,url,tokenize_content,sentiment) values(%s,%s)"
    args = (content, published, created, url, tokenize_content, sentiment)
    mycursor.execute(query,args)
    return None

def get_postID(url=""):
    query = "select id from posts where url = '{}'".format(url)
    check_postID = mycursor.execute(query)
    return check_postID
def insert_post_tags(postId="",symbol="", keywordName=""):
    query = "insert into post_tags(postID,symbol,keywordName) values(%s,%s,%s)"
    args = (postId,symbol,keywordName)
    mycursor.execute(query,args)
    return None




