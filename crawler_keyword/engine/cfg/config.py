CHROME_PATH = "http://127.0.0.1:4444/wd/hub"
LOGGING_PATH = "./logging"

SENTIMENT_MODEL_PATH = "/home/hatt2/news_crawl/crawler_keyword/engine/model/model.pkl"
IMAGE_PATH = "/home/hatt2/news_crawl/crawler_keyword/engine/image/"

ELASTIC_CONFIG = {
    "host": "192.168.41.19",
    "port": "9200"
}

MYSQL_CONFIG = {
    "host": "localhost",
    "port": "13306",
    "user": "sentiment",
    "passwd": "123456",
    "database": "sentiment",
}

config = {
    "ndh": {
        "pagination_url": "https://ndh.vn/search.html?q={:s}&page={:d}.html",
        "page_url": "https://ndh.vn/search.html?q={$keyword$}&page={$page$}.html",
        "xpath": {
            "post_links": "//div[@class='list-news']//article[@class='item-news']//h3[@class='title-news']//a",
            "post_dates": "//span[@class='time-public']",
            "title": "//h1[@class='title-detail']",
            "summary": "//p[@class='related-news']",
            "image_url": "//article[@class='fck_detail']//img", 
            "content": "//article[@class='fck_detail']",
            "date": "//span[@class='date-post']",
            "date_extract_regex": "([0-9]*?\/[0-9]*?\/[0-9]*)",
            "date_element_split_by": "/",
            "author": "",
        }
    },
    "vnexpress":{
        "pagination_url": "https://timkiem.vnexpress.net/?q={:s}&page={:d}",
        "page_url": "https://timkiem.vnexpress.net/?q={$keyword$}&page={$page$}",
        "xpath": {
            "post_links": "//div[@class='width_common list-news-subfolder']//article[@class='item-news item-news-common']//h3[@class='title-news']//a",
            "date": "//span[@class='date']",
            "title": "//h1[@class='title-detail']",
            "summary": "//p[@class='description']",
            "image_url": "//div[@class='fig-picture']//img",
            "content": "//article[@class='fck_detail ']",
            "date_extract_regex": "([0-9]*?\/[0-9]*?\/[0-9]*)",
            "date_element_split_by": "/",
        }
    }
    
}
config_1 = {
    "https://cafef.vn":{
        "pagination_url": "https://cafef.vn/search/dmNi/{:s}/trang-{:d}.chn",
        "page_url": "https://cafef.vn/search/dmNi/{$keyword$}/trang-{$page$}.chn",
        "xpath": {
            "post_links": "//div[@class='list_news clearfix']//div[@class='search-content-wrap']//ul[@class='timeline list-bytags']//li[@class='item']//h4[@class='titlehidden']//a",
            "date": "//span[@class='pdate']",
            "title": "//h1[@class='title']",
            "summary":"//h2[@class='sapo']",
            "image_url": "//div[@class ='media']//img",
            "content": "//div[@class='contentdetail']//span[@id='mainContent']",
        }
    }
}

