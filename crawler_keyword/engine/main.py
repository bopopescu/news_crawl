import utils.crawler_v2 as crawler
import time

begin = time.time()

print(crawler.crawl(source="https://ndh.vn",keyword="cổ phiếu",exit_when_url_exist=False,date_range=("17/5/2020","19/5/2020")))

end = time.time()

print("Done. Time taken: "+str(end-begin))