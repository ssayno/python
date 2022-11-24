import asyncio
import aiohttp
import aiofiles
import os
import time


BASE_URL = 'http://flupy.org/data/flags'
POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
DEST_DIR = 'downloads/'


if not os.path.exists(DEST_DIR):
    os.mkdir(DEST_DIR)


async def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    async with aiofiles.open(path, 'wb') as fp:
        await fp.write(img)
    return True


async def download_one(session, cc):
    try:
		print(cc, end=' ')
		url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
		async with session.get(url) as resp:
			image = await resp.read()
			await save_flag(image, cc.lower() + '.gif')
    except:
        print('?')
    return True

async def main():
    t0 = time.time()
    session = aiohttp.ClientSession()
    task_ = (
        download_one(session, item) for item in POP20_CC
    )
    print("开始")
    await asyncio.gather(*task_)
    await session.close()
    elapsed = time.time() - t0
    msg = '{} flags downloaded in {:.2f}s'
    print(msg.format(len(POP20_CC), elapsed))
    return True


async def main__():
    t0 = time.time()
    async with aiohttp.ClientSession() as session:
    	for item in POP20_CC:
    		url ='{}/{cc}/{cc}.gif'.format(BASE_URL, cc=item.lower())
    		async with session.get(url) as resp:
    			await save_flag(await resp.read(), item.lower() + '.gif')
    elapsed = time.time() - t0
    msg = '{} flags downloaded in {:.2f}s'
    print(msg.format(len(POP20_CC), elapsed))




if __name__ == '__main__':
	asyncio.run(main())
