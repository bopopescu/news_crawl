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

wd_options = Options()
wd_options.add_argument("--headless")
wd_options.add_argument('--no-sandbox')
wd_options.add_argument('--disable-dev-shm-usage')

# wd = webdriver.Remote(CHROME_PATH, DesiredCapabilities.CHROME,options=wd_options)
# wd = webdriver.Chrome("./engine/chromedriver", options=wd_options)

def get_post_content_from_link(source="", post_link="", keyword="", symbol=""):
    wd = webdriver.Remote(CHROME_PATH, DesiredCapabilities.CHROME,options=wd_options)

    data = {
        "keyword": keyword,
        "symbol": symbol,
        "url": "",
        "title": "",
        "summary": "",
        "image_url": "",
        "content": "",
        "date": "",
        "author": "",
        "tokenize_content": "",
        "created": "",
    }
    data["url"] = post_link
    wd.get(post_link)

    try:
        title = wd.find_element_by_xpath(
            config[source]["xpath"]["title"]
        ).get_attribute("innerText")
        data["title"] = title
        print("TITLE",title)
    except Exception as e:
        print("Warning: Can't fetch title "+str(e))

    try:
        content = wd.find_element_by_xpath(
            config[source]["xpath"]["content"]).get_attribute("innerText")
        data["content"] = data_handler.prepare_content(content)
    except Exception as e:
        print("Warning: Can't fetch content "+str(e))

    try:
        summary = wd.find_element_by_xpath(
            config[source]["xpath"]["summary"]).get_attribute("innerText")
        data["summary"] = data_handler.prepare_content(summary)
    except Exception as e:
        print("Warning: Can't fetch summary "+str(e))

    try:
        image_url = wd.find_element_by_xpath(
            config[source]["xpath"]["image_url"]).get_attribute("src")
        data["image_url"] = data_handler.prepare_content(image_url)
    except Exception as e:
        print("Warning: Can't fetch image_url "+str(e))

    try:
        date = wd.find_element_by_xpath(
            config[source]["xpath"]["date"]).get_attribute("innerText")
        data["date"] = data_handler.convert_to_mysql_datetime(date)
    except Exception as e:
        print("Warning: Can't fetch date "+str(e))

    try:
        author = wd.find_element_by_xpath(
            config[source]["xpath"]["author"]).get_attribute("innerText")
        data["author"] = author
    except Exception as e:
        print("Warning: Can't fetch author "+str(e))

    try:
        tokenize_content = data_handler.tokenize_content(data["content"])
        data["tokenize_content"] = tokenize_content
    except Exception as e:
        print("Warning: Can't tokenize content "+str(e))
    
    try:
        created = datetime.datetime.now()
        data["created"] = created
    except Exception as e:
        print("Warning: Can't get datetime" + str(e))
        
    wd.close()
    return data



"""
Find the page range given a specific date
date_range is a 2-string-elements tuple, format (d/m/y, d/m/y)
"""


def find_page_range(source, keyword, from_page, to_page, date_range):
    wd = webdriver.Remote(CHROME_PATH, DesiredCapabilities.CHROME,options=wd_options)

    if date_range == None:
        return (from_page, to_page)

    page_url = config[source]["page_url"].replace("{$keyword$}", keyword)
    xpath_configuration = config[source]["xpath"]
    date_extract_regex = xpath_configuration["date_extract_regex"]
    date_element_split_by = xpath_configuration["date_element_split_by"]
    date_from_tuple = date_range[0].split(date_element_split_by)
    date_from_tuple.reverse()
    date_from_tuple = [int(elem) for elem in date_from_tuple]
    date_to_tuple = date_range[1].split(date_element_split_by)
    date_to_tuple.reverse()
    date_to_tuple = [int(elem) for elem in date_to_tuple]

    page_limit_left = from_page
    page_limit_right = to_page

    """
    Find the to_page - the last page which contains posts in date_range
    """
    lpage = from_page
    rpage = to_page
    while True:
        if lpage >= rpage:
            if lpage == rpage:
                page_limit_right = lpage
            else:
                page_limit_right = -1
            break
        mid_page = int((lpage + rpage) / 2 + 1)
        url = page_url.replace("{$page$}", str(mid_page))
        wd.get(url)
        link_elements = wd.find_elements_by_xpath(
            xpath_configuration["post_links"])
        links = [link_element.get_attribute("href")
                 for link_element in link_elements]

        if len(links) == 0:
            rpage = mid_page-1
            continue

        post_data = get_post_content_from_link(
            source=source, post_link=links[0], keyword=keyword)

        date_cur = re.findall(date_extract_regex, post_data["date"])
        if len(date_cur) == 0:
            rpage = mid_page - 1
        else:
            date_cur_tuple = date_cur[0].split(date_element_split_by)
            date_cur_tuple.reverse()
            date_cur_tuple = [int(elem) for elem in date_cur_tuple]
            if date_cur_tuple < date_from_tuple: # if current date is older than the range
                rpage = mid_page-1
            else:
                lpage = mid_page
    """"""

    """
    Find the from_page - the first page which contains posts in date_range
    """
    lpage = from_page
    rpage = page_limit_right
    while True:
        if lpage >= rpage:
            if lpage == rpage:
                page_limit_left = lpage
            else:
                page_limit_left = -1
            break
        mid_page = int((lpage + rpage) / 2)
        url = page_url.replace("{$page$}", str(mid_page))
        wd.get(url)
        link_elements = wd.find_elements_by_xpath(
            xpath_configuration["post_links"])
        links = [link_element.get_attribute("href")
                 for link_element in link_elements]

        if len(links) == 0:
            rpage = mid_page-1
            continue

        post_data = get_post_content_from_link(
            source=source, post_link=links[0], keyword=keyword)

        date_cur = re.findall(date_extract_regex, post_data["date"])
        if len(date_cur) == 0:
            rpage = mid_page - 1
        else:
            date_cur_tuple = date_cur[-1].split(date_element_split_by)
            date_cur_tuple.reverse()
            date_cur_tuple = [int(elem) for elem in date_cur_tuple]
            if date_cur_tuple > date_to_tuple: # if current date is older than the range
                lpage = mid_page+1
            else:
                rpage = mid_page

    print("FROM PAGE",page_limit_left,"TO PAGE:",page_limit_right)
    
    wd.close()
    return (page_limit_left, page_limit_right)


def crawl(source="",symbol="", keyword="", from_page=1, to_page=10000, exit_when_url_exist=True, date_range=None):
    wd = webdriver.Remote(CHROME_PATH, DesiredCapabilities.CHROME,options=wd_options)
    
    
    print("CRAWLING FROM SOURCE {:s}".format(source))
    new_record = 0
    msg = ""

    xpath_configuration = config[source]["xpath"]
    page_url = config[source]["page_url"].replace("{$keyword$}", keyword)

    """
    Find the starting page and ending page if date_range is provided
    """
    (start_page, end_page) = find_page_range(source=source, keyword=keyword,
                                             from_page=from_page, to_page=to_page, date_range=date_range)

    from_page = max(from_page, start_page)
    to_page = min(to_page, end_page)
    """
    End of finding starting and ending page
    """

    if db.connection_available():
        print("Scraping page", from_page, to_page)
        exit_because_url_exist = False

        for page in range(from_page, to_page+1):
            if exit_because_url_exist:
                break

            url = page_url.replace("{$page$}", str(page))
            print("GETTING ", url)
            wd.get(url)
            link_elements = wd.find_elements_by_xpath(
                xpath_configuration["post_links"]
            )
            links = [link_element.get_attribute("href") for link_element in link_elements]

            for link in links:
                print("get data from :", link)
                data = get_post_content_from_link(
                    source=source, post_link=link, keyword=keyword, symbol=symbol
                )
                postid = db.get_postID(url=link)
                print("POST ID",postid)
                if postid is None:
                    db.insert_content_to_mysql(title=data["title"], summary=data["summary"], published=data["date"], created=data["created"] ,url=link ,image_url=data["image_url"], tokenize_content=data["tokenize_content"])
                    new_record += 1
                    postid = db.get_postID(url=link)
                    filtered_sentences = data_handler.get_sentences_contain_symbol(data["tokenize_content"],symbol)
                    print("filtered sentences:",len(filtered_sentences))
                    for sent in filtered_sentences:
                        print(sent)
                    for sentence in filtered_sentences:
                        sentence_sentiment = ""
                        try:
                            sentence_sentiment = data_handler.sentiment(sentence)
                        except Exception as e:
                            print("Cannot sentiment sentence "+str(e))
                        db.insert_post_tags(postId=postid, content=sentence, symbol=symbol, sentiment=sentence_sentiment)
            
    else:
        msg = "Cannot connect to mysql"

    wd.close()

    return {
        "new_record": new_record,
        "msg": msg
    }


