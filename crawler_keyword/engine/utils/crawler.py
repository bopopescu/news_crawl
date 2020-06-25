# DEPRACATED
import platform
import utils.elastic as es
import time
import utils.data as data_handler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from cfg.config import config,CHROME_PATH
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


wd_options = Options()
wd_options.add_argument("--headless")
wd_options.add_argument('--no-sandbox')
wd_options.add_argument('--disable-dev-shm-usage')        

wd = webdriver.Remote(CHROME_PATH, DesiredCapabilities.CHROME,options=wd_options)


# get all new links which are not existing on elastic search
def get_new_links(source="",keyword="",from_page=1,to_page=10000,exit_when_url_exist=True,date_range=None):
    page = from_page

    document_exist_in_elastic = False
    post_urls = []
    pagination_url = config[source]["pagination_url"]
    xpath_configuration = config[source]["xpath"]
    es_index = config[source]["elastic_index"]

    # if need to find posts in a specific range, find the actual from_page and to_page
    if date_range:
        # find actual from_page
        page_url = pagination_url.format(keyword,from_page)

        wd.get(page_url)
        post_dates = wd.find_elements_by_xpath(xpath_configuration["post_dates"])
        
        # find actual to_page
        pass

    while True:
        if page > to_page:
            print("Page reach limit")
            break

        if document_exist_in_elastic and exit_when_url_exist:
            print("Link existed")
            break

        page_url = pagination_url.format(keyword,page)

        wd.get(page_url)
        post_links = wd.find_elements_by_xpath(xpath_configuration["post_links"])

        if len(post_links) == 0:
            print("Cannot find new links. Terminating...")
            break
        
        for link in post_links:
            post_url = link.get_attribute("href")
            print(post_url)
            if es.document_exists(es_index=es_index,url=post_url):
                document_exist_in_elastic = True
                if exit_when_url_exist:
                    break

            post_urls.append(post_url)
        
        page += 1
    
    return post_urls


def get_post_content_from_link(source="",post_link="",keyword=""):
    data = {
        "keyword": keyword,
        "url": "",
        "title": "",
        "content": "",
        "date": "",
        "author": "",
        "tokenize_content": "",
    }
    data["url"] = post_link
    wd.get(post_link)
    try:
        title = wd.find_element_by_xpath(config[source]["xpath"]["title"]).get_attribute("innerHTML")
        data["title"] = title
    except Exception as e:
        print("Can't fetch title "+str(e))
        pass
    
    try:
        content = wd.find_element_by_xpath(config[source]["xpath"]["content"]).get_attribute("innerHTML")
        data["content"] = data_handler.prepare_content(content)
    except Exception as e:
        print("Can't fetch content "+str(e))
        pass

    try:
        date = wd.find_element_by_xpath(config[source]["xpath"]["date"]).get_attribute("innerHTML")
        data["date"] = date
    except Exception as e:
        print("Can't fetch date "+str(e))
        pass

    try:
        author = wd.find_element_by_xpath(config[source]["xpath"]["author"]).get_attribute("innerHTML")
        data["author"] = author
    except Exception as e:
        print("Can't fetch author "+str(e))
        pass

    try:
        tokenize_content = data_handler.tokenize_content(data["content"])
        data["tokenize_content"] = tokenize_content
    except Exception as e:
        print("Can't tokenize content "+str(e))
        pass
    
    return data


def crawl(source="",keyword="",from_page=1,to_page=10000,exit_when_url_exist=True,date_range=(None,None)):
    new_record = 0
    msg = ""

    if es.connection_is_available():
        new_links = get_new_links(
            source=source,
            keyword=keyword,
            from_page=from_page,
            to_page=to_page,
            exit_when_url_exist=exit_when_url_exist)
        print(new_links)
        for link in new_links:
            print("Getting content for "+link)
            post_data = get_post_content_from_link(source=source,post_link=link,keyword=keyword)
            es.add_document(es_index=config[source]["elastic_index"],data=post_data)
            new_record += 1
    else:
        msg = "Cannot connect to elastic search"
    
    return {
        "new_record": new_record,
        "msg": msg
    }

