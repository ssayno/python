#!/usr/bin/env python3
import os
import sys
import time

import requests
from concurrent import futures

POP20_CC = ('CN', 'IN', 'US', 'ID', 'BR', 'PK', 'NG', 'BD', 'RU', 'JP',
            'MX', 'PH', 'VN', 'ET', 'EG', 'DE', 'IR', 'TR', 'CD', 'FR')
url = 'http://flupy.org/data/flags'
Max_workers = 20
dest_dir = "./Pictures2"


def save_fig(img, filename):
    path = os.path.join(dest_dir, filename)
    with open(path, 'wb') as f:
        f.write(img)


def get_flag(cc):
    url2 = f'{url}/{cc.lower()}/{cc.lower()}.gif'
    resp = requests.get(url2)
    return resp


def show(text):
    print(text, end=" ")
    sys.stdout.flush()


def download_pic(cc):
    img = get_flag(cc).content
    show(cc)
    save_fig(img, f"{cc.lower()}.gif")


def downloads(cc_list):
    with futures.ThreadPoolExecutor(Max_workers) as executor:
        res = executor.map(download_pic, sorted(cc_list))
    return len(cc_list)


def main():
    t0 = time.time()
    count = downloads(POP20_CC)
    haoshi = time.time() - t0
    print(f"\n{count} flag spend {haoshi} seconds")


if __name__ == '__main__':
    main()