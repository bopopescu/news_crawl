# KEYWORD CRAWLER

Post crawler by keyword

## Getting Started

### Technologies

1. Python
2. Headless browser selenium
3. Elastic search
4. Kibana

### Prerequisites

1. Docker version 19.03.8
2. docker-compose version 1.25.4
3. Python 3 

### Installing

A step by step series of examples that tell you how to get a development env running

Set up the environment with docker-compose

```
docker-compose up
```

Install python packages

```
pip install -r requirements.txt
```

Configure mysql credential in `./engine/cfg/config.py`


## Running the crawler

Run the crawler by executing


```
python ./engine/main.py
```


## Running the crawler with crontab

```
0 0 * * * {YOUR_BASE_PATH}/crawler_keyword/engine/fetch.sh
```

## Customize the crawler

Customize the crawler in ```main.py```
```
crawler.crawl(source="https://ndh.vn",keyword="cổ phiếu",from_page=499,exit_when_url_exist=False)
```
```source```: ```string``` - The source of the posts. Configuration in ```./cfg/config.py```

```keyword```: ```string``` - The keyword used for search

```from_page```: ```int``` - The start page which posts will be fetched from 

```exit_when_url_exist```: ```bool``` - If set to ```False```, the crawler will exit if it see a url which has been indexed in elastic search
```date_range```: ```tuple``` - (from_date, to_date), the date range which we want to fetch the posts. The format of from_date and to_date will be "d/m/y", eg "7/5/2020"

## Working with elastic search

Get indexed documents

```
GET http://localhost:9200/posts/_search/?pretty=true&from=[FROM_INDEX]&size=[SIZE_OF_RETURN_OBJECTS]
```

```FROM_INDEX```: number which indicates the starting point of the return results

```SIZE_OF_RETURN_OBJECTS```: the size of the returned ```hits``` array 

## Author
proxyht
