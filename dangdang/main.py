#!/usr/bin/env python
import requests
import time
from bs4 import BeautifulSoup
import pymysql
from concurrent import futures


def get_attr(url):
    targets = []
    response = requests.get(url=url)
    if response.status_code != 200:
        print("can't connect the web", response.status_code)
        return []
    data = response.text
    html = BeautifulSoup(data, 'html.parser')
    ul = html.find(id='component_59')
    for li in ul.find_all(name='li'):
        target = {}
        target['bookname'] = li.a.attrs['title'].strip(' ')
        target['price'] = float(li.find(class_="search_now_price").string.strip('¥'))
        # print("\n", li.a.attrs['title'], li.find(class_="search_now_price").string.strip('¥'), end=" ")
        informations = li.find(class_="search_book_author").find_all(name="span")
        try:
            target['author'] = informations[0].find(name='a').string
        except AttributeError:
            target['author'] = 'Unknow'
        try:
            target['data'] = informations[1].string.replace(' /', '')
        except AttributeError:
            target['data'] = 'Unknow'
        try:
            target['public'] = informations[2].find(name='a').attrs['title']
        except AttributeError:
            target['public'] = 'Unknow'
        targets.append(target)
    return targets


def connectMySQL(target):
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='271xufei.',
                         database='python')
    cursor = db.cursor()
    cursor.execute('show tables;')
    databases = cursor.fetchall()
    if ('books', ) not in databases:
        create_table = """create table if not exists books(
            bookname varchar(128) primary key,
            price float not null,
            author varchar(32) not null,
            data varchar(20) not null,
            public varchar(20) not null
            )
            """
        try:
            cursor.execute(create_table)
            db.commit()
        except Exception as e:
            db.rollback()

    insert_value = 'insert into books values ("{}", "{}","{}", "{}", "{}")'
    try:
        cursor.execute(insert_value.format(target['bookname'], target['price'],
                                           target['author'], target['data'], target['public']))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

    db.close()


if __name__ == '__main__':
    start = time.time()
    url = 'http://search.dangdang.com/?key=python&act=input'
    url_list = [f'{url}&page_index={item}' for item in range(1, 101)]
    for item in url_list:
        with futures.ThreadPoolExecutor(max_workers=1000) as executor:
            executor.map(connectMySQL, get_attr(item))

    spend = time.time() - start
    print(f"花费时间为{spend}")
