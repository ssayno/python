#!/usr/bin/env python3
import asyncio
from html import unescape
import unicodedata
from collections import OrderedDict
import os
import requests
import aiohttp
import aiofiles
import re
import time


def get_chapter_url(url):
    resp = requests.get(url, headers=headers)
    print(resp.status_code)
    with open("resp.html", 'w+', encoding='gbk') as f:
        f.write(resp.content.decode('gbk'))
    half_urls = re.findall(r'<li><a href="(.*[.]html)" .*>(.*?)</a>', resp.text)
    title_urls = OrderedDict()
    for half_url in reversed(half_urls):
        title = half_url[1]
        if "月票" in title or "暂停一天" in title:
            continue
        entire_url = url + half_url[0].split("/")[-1]
        title_urls[title] = entire_url
    return title_urls

async def track_single(session, url, title, count):
    title = re.sub('\s+', "-", title)
    # print("Current chapter is", title)
    async with session.get(url, headers=headers) as resp:
        dc = resp.headers['content-type'].split(";")[1].split("=")[1]
        try:
            content = await resp.text(encoding='gbk')
        except:
            try:
                content = await resp.text(encoding='latin-1')
            except Exception as e:
                print(e)
                print(url)
                return
        p_tags = re.findall('<p>(.*?)<p>', content, flags=re.DOTALL)
        if not p_tags:
            p_tags = re.findall('<br />(.+?)<br />', content, flags=re.DOTALL)
            #print(content)
            # print(p_tags)
        output_tex = os.path.join(
            OUTPUT_DIR, f'{count}-{title}.tex'
        )
        async with aiofiles.open(output_tex, 'w+') as pwf:
            writed_content = fr'\chapter{{{title}}}\n'
            for p_tag in p_tags:
                if "div" in p_tag:
                    continue
                unicode_p_tag = unicodedata.normalize(
                    "NFKD", unescape(p_tag)
                )
                after_purity_p_tag = re.sub("UU看书 www.uukanshu.com", "", unicode_p_tag)
                # print(after_purity_p_tag)
                writed_content += fr'{after_purity_p_tag}\par{{}}'
            await pwf.write(writed_content)
        time.sleep(0.3)
    # print(f"Chapter {title} finished!")


async def main():
    count = 1
    tasks = []
    session = aiohttp.ClientSession()
    pw_url = 'https://www.uukanshu.com/b/10079/'
    results = get_chapter_url(pw_url)
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
        'Cookie': 'fcip=111; ASP.NET_SessionId=i4leaur5mqxefo3trzji23br; _ga=GA1.2.449041969.1670993333; _gid=GA1.2.399933037.1670993334; __gads=ID=cb6ad9a8a8d1c94b-228aa9ea47d8001d:T=1670993334:RT=1670993334:S=ALNI_MYD-bIAI9xO5bI0gdzTUOFmq-pRxA; __gpi=UID=00000911db4bf09f:T=1670993334:RT=1670993334:S=ALNI_Mahv4UgvAx8k5OPaEocSQ804CkjQg; __atssc=google%3B3; lastread=10079%3D5155%3D%u5E8F%u7AE0%20%u5927%u8352; __atuvc=8%7C50; __atuvs=639955b4bcb1788d007; _gat=1; FCNEC=%5B%5B%22AKsRol-MtVY6DjcAWr3aakYtqC6UH_gahLANcUR-XwcNbWKWvOe3j-NEMla3gJLKv9tE_nrBsWxb8HLXGDJrBecSHzk2Y6sm98KMFcnuVnDgEPbf75bITkg2GRnCRQ83-M5v1g4DJZVzCIK3HMxYcEr5b2kUhWS1Ew%3D%3D%22%5D%2Cnull%2C%5B%5D%5D'
    }
    OUTPUT_DIR = os.path.join(
        os.path.dirname(__file__), "Perfect-World-TeX"
    )
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    asyncio.run(main=main())
