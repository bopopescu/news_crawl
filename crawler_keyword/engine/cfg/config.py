CHROME_PATH = "http://127.0.0.1:4444/wd/hub"
LOGGING_PATH = "./logging"

SENTIMENT_MODEL_PATH = "/model/model.pkl"

ELASTIC_CONFIG = {
    "host": "192.168.41.19",
    "port": "9200"
}

MYSQL_CONFIG = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "passwd": "",
    "database": "sentiment",
}

config = {
    "https://ndh.vn": {
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
    }
}