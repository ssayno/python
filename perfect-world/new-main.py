#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from html import unescape
import unicodedata
from collections import OrderedDict
import re
import aiofiles
import aiohttp
import asyncio
import os


def get_chapter_url(url):
    resp = requests.get(url)
    print(resp.status_code)
    half_urls = re.findall(r'<li><a href="(.*[.]html)" .*>(.*?)</a>', resp.content.decode('U8'))
    title_urls = OrderedDict()
    for half_url in half_urls:
        title = half_url[1]
        if "月票" in title or "暂停一天" in title:
            continue
        entire_url = half_url[0]
        title_urls[title] = entire_url
    return title_urls



async def track_single(session, url, title, count):
    title = re.sub(
        '\s+', "-", ' '.join(title.split(' ')[1:])
    )
    async with session.get(url, headers=headers) as resp:
        soup = BeautifulSoup(await resp.text(encoding='U8'), 'lxml')
        p_tags = soup.select('#neirong > p')
        output_tex = os.path.join(
            OUTPUT_DIR, f'{count}-{title}.tex'
        )
        async with aiofiles.open(output_tex, 'w+') as pwf:
            writed_content = f'\chapter{{{title}}}\n'
            for p_tag in p_tags:
                p_tag = p_tag.text
                if "div" in p_tag:
                    continue
                unicode_p_tag = unicodedata.normalize(
                    "NFKD", unescape(p_tag)
                )
                after_purity_p_tag = unicode_p_tag.replace(
                    '\\', ''
                ).replace(
                    '$', '\$'
                ).replace(
                    '%', '\%'
                ).replace(
                    '_', '\_'
                ).replace(
                    '~', '\textasciitide{}'
                ).replace(
                    '#', '\#'
                ).replace(
                    '&', '\&'
                ).replace(
                    '^', '\^'
                )
                # print(after_purity_p_tag)
                writed_content += fr'{after_purity_p_tag}\par{{}}'
            await pwf.write(writed_content)
    await asyncio.sleep(1)


async def main():
    count = 1
    tasks = []
    session = aiohttp.ClientSession()
    url = 'https://www.51shucheng.net/xuanhuan/wanmeishijie'
    results = get_chapter_url(url)
    # await track_single(session, 'https://www.uukanshu.com/b/10079/5155.html', "a")
    for title, url in results.items():
        tasks.append(track_single(
            session=session, url=url, title=title, count=count
        ))
        count += 1
    await asyncio.gather(*tasks)
    await session.close()


if __name__ == '__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Cookie': " __gads=ID=971e62723feb4d1c-22f54a8752d8007a:T=1670993392:RT=1670993392:S=ALNI_MZh7IjZNlkYgOe8Du1YwcjKfcdwEA; __gpi=UID=00000911dad6a2aa:T=1670993392:RT=1670993392:S=ALNI_MaPX1D7Rv0yuBRSKRVbtv706wozdQ; _gid=GA1.2.340554420.1670993393; fontsize=0; _ga_4QEWBNE9J8=GS1.1.1671001286.2.1.1671001553.0.0.0; _ga=GA1.2.69592289.1670993392"
    }

    OUTPUT_DIR = os.path.join(
        os.path.dirname(__file__), "Perfect-World-TeX"
    )
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    asyncio.run(main())
