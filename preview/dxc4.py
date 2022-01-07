#!/usr/bin/python
import requests
from lxml import etree
import re
from concurrent import futures
from bs4 import BeautifulSoup
import time


def qParse(url):
    data = requests.get(url)
    if data.status_code == 200:
        data = data.content.decode('utf8')
        data = BeautifulSoup(data, 'html.parser')
        results = data.select('#content')[0]
        more = data.select('#content > p')[0]
        # results = data.xpath('//div[@id="content"]/text()')
        title = data.select('#wrapper > div.content_read > div > div.bookname > h1')[0].string
        print(title)
        # title = data.xpath('//*[@id="wrapper"]/div[4]/div/div[1]/a[2]/@href')
        # print(results.get_text(), type(results.get_text()), len(results.get_text()))
        # print(more.get_text())
        with open(f'./passage4/{title}.txt', 'w') as f:
            f.write(results.get_text().strip(more.get_text()).replace('\xa0', ''))
        # for result in results:
        #     print(result.string)
        #     continue
        #     if not re.match('\r', result):
        #         with open(f'./passage/第{title}章.txt', 'w') as f:
        #             f.write(result.replace('\xa0', ''))
        #             # print(result.replace('\xa0', ''))
        #         # print(result.strip('\xa0\xa0\xa0\xa0'))
    else:
        print(f"connect error, status_code is {data.status_code}")


def getLength(url):
    data = requests.get(url)
    if data.status_code == 200:
        data = etree.HTML(data.content.decode('utf8'))
        lists = data.xpath('//div[@id="list"]/dl/dd/a/@href')
        return lists
    print(f"connect error, status_code is {data.status_code}")


if __name__ == '__main__':
    start = time.time()
    url = 'https://www.xbiquge.la/23/23811/'
    lists = getLength(url)
    lists = [url + item.split('/')[-1] for item in lists]
    # with futures.ThreadPoolExecutor(max_workers=100) as executor:
    #     executor.map(qParse, lists)
    for list_url in lists:
        qParse(list_url)
    spend = time.time() - start

    print(f"花费时间为{spend}")
