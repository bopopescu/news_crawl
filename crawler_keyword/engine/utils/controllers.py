import re
import platform
import time
import datetime
import utils.data as data_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cfg.config import config, CHROME_PATH
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
from cfg.config import config
import utils.mysqlutils as db
from utils.redisquene import RedisQueue
from sentence_splitter import SentenceSplitter, split_text_into_sentences

q = RedisQueue()
splitter = SentenceSplitter(language='en')
sentiment = data_handler.sentiment
def controller():
    data = q.get()
    url = data[b'url'].decode('utf8')
    content = data[b'content'].decode('utf8')
    tokenize_content = data[b'tokenize_content'].decode('utf8')
    symbol = data[b'symbol'].decode('utf8')
    summary = data[b'summary'].decode('utf8')
    date = data[b'date'].decode('utf8')
    image_url = data[b'image'].decode('utf8')
    title = data[b'title'].decode('utf8')
    created = data[b'created'].decode('utf8')
    postid = db.get_postID(url=url)
    list_keywords = db.get_keywords_by_stock_ticket(stock_ticket=symbol)
    print("POST ID",postid)
    if postid is None:
        db.insert_content_to_mysql(title=title, summary=summary, published=date, created=created ,url=url ,image_url=image_url, tokenize_content=tokenize_content,content = content)
        print(url)
        get_postid = db.get_postID(url=url)
        print("NEW POST ID",get_postid)

        doclist = data_handler.get_sentences_contain_keywords(text=content,keywords=list_keywords)

        print("LIST KW",list_keywords)
        docstr = " ".join(doclist)
        tokenize_docstr = data_handler.tokenize_content(docstr)
        print("TOKENIZE DOCSTR",tokenize_docstr)
        
        if len(tokenize_docstr) > 0:
            sentiment_of_symbol = sentiment(tokenize_docstr)
            db.insert_post_tags(postId=get_postid, content=tokenize_docstr, symbol=symbol, sentiment=sentiment_of_symbol)
        else:
            sentiment_of_symbol = sentiment(tokenize_content)
            db.insert_post_tags(postId=get_postid, content=content, symbol=symbol, sentiment=sentiment_of_symbol)
    else:
        check_post_tag = db.check_post_tag(postId=postid, symbol=symbol)
        if check_post_tag is None:
            doclist = data_handler.get_sentences_contain_keywords(text=content,keywords=list_keywords)
            print("LIST KW",list_keywords)
            
            docstr = " . ".join(doclist)
            tokenize_docstr = data_handler.tokenize_content(docstr)
            print("TOKENIZE DOCSTR",tokenize_docstr)

            if len(tokenize_docstr) > 0:
                sentiment_of_symbol = sentiment(tokenize_docstr)
                db.insert_post_tags(postId=postid, content=tokenize_docstr, symbol=symbol, sentiment=sentiment_of_symbol)
            else:
                sentiment_of_symbol = sentiment(tokenize_content)
                db.insert_post_tags(postId=postid, content=tokenize_content, symbol=symbol, sentiment=sentiment_of_symbol)
        else:
            pass
    