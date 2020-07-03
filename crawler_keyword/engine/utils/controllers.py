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
def controller():
    data = q.get()
    url = data[b'url'].decode('utf8')
    content = data[b'content'].decode('utf8')
    tokenize_content = data[b'tokenize_content'].decode('utf8')
    symbol = data[b'symbol'].decode('utf8')
    summary = data[b'summary'].decode('utf8')
    date = data[b'date'].decode('utf8')
    image_url = data[b'image_url'].decode('utf8')
    title = data[b'title'].decode('utf8')
    created = data[b'created'].decode('utf8')
    postid = db.get_postID(url=url)
    list_keywords = db.get_keywords_by_stock_ticket(stock_ticket=symbol)
    print("POST ID",postid)
    if postid is None:
        db.insert_content_to_mysql(title=title, summary=summary, published=date, created=created ,url=url ,image_url=image_url, tokenize_content=tokenize_content)
        get_postid = db.get_postID(url=url)
        doclist_of_symbol = []
        clean_content = content.replace(',',' ')
        sentences_of_content = splitter.split(clean_content)
        for i in sentences_of_content:
            res = [ele for ele in list_keywords if(ele in i)]
            if res == []:    
                pass
            else:
                doclist= doclist_of_symbol.append(i)
                docstr = ' '.join(doclist)
        output = docstr
        tokenize_docstr = tokenize_content(output)
        sentiment_of_symbol = sentiment(tokenize_docstr)
        db.insert_post_tags(postId=get_postid, content=output, symbol=symbol, sentiment=sentiment_of_symbol)
    else:
        doclist_of_symbol = []
        clean_content = content.replace(',',' ')
        sentences_of_content = splitter.split(clean_content)
        for i in sentences_of_content:
            res = [ele for ele in list_keywords if(ele in i)]
            if res == []:    
                pass
            else:
                doclist=doclist_of_symbol.append(i)
                docstr_of = ' '.join(doclist)
        output = docstr_of
        tokenize_docstr = tokenize_content(output)
        sentiment_of_symbol = sentiment(tokenize_docstr)
        db.insert_post_tags(postId=postid, content=output, symbol=symbol, sentiment=sentiment_of_symbol)
            
        
        
    
    
    