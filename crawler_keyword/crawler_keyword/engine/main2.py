import utils.crawler_v3 as crawler
import time

begin = time.time()

print(crawler.crawlSQL(source="https://ndh.vn", symbol= "ACB",keyword="cổ phiếu ACB",date_range=("17/5/2020","19/5/2020")))

end = time.time()

print("Done. Time taken: "+str(end-begin))