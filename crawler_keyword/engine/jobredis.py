import sys
import utils.crawler_v3 as crawler
import utils.mysqlutils as database
import time
from datetime import date
from cfg.config import config as sources
import utils.mysqlutils as db

begin = time.time()

try:
    time_start_crawl = sys.argv[1]
    time_end_crawl = sys.argv[2]
except:
    print("No arguments provided. Fetching posts from today")
    today = "/".join([str(date.today().day), str(date.today().month), str(date.today().year)])
    time_start_crawl = today
    time_end_crawl = today

stock_indexes = db.get_all_stock_ticket()
for stock_index in stock_indexes:
    print("FETCHING STOCK {}".format(stock_index))
    keywords = database.get_keywords_by_stock_ticket(stock_index)
    for keyword in keywords:
        print("     Looking for keyword {}".format(keyword))
        for source in sources:
            print(crawler.crawl(source=source,symbol=stock_index,from_page=1,to_page=10,keyword=keyword,exit_when_url_exist=False,date_range=(time_start_crawl,time_end_crawl)))

end = time.time()

print("Done. Time taken: "+str(end-begin))