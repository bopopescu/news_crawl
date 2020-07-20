# News Crawl
## Architecture
## How to run:
- ```cd crawler_keyword ```
- Build image:```cd crawler_keyword/engine```, ```docker build -f Dockerfile.crawler -t crawler .```, ```docker  build -f Dockerfile.controller -t crawler```
- Run compose : ```cd ..```,```docker-compose up```
- Connect to the Mysql port 3308 import ```db.sql```, data to mysql.
