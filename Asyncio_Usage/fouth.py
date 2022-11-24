#!/usr/bin/env python3
import asyncio
import time

# time.strftime('%H:%M:%S')
async def sleep_normal():
    print(f"normal sleep start {time.strftime('%H:%M:%S')}")
    # time.sleep(2)
    await asyncio.sleep(2)
    print(f"normal sleep end {time.strftime('%H:%M:%S')}")


async def sleep_async():
    print(f"async sleep start {time.strftime('%H:%M:%S')}")
    # time.sleep(2)
    await asyncio.sleep(2)
    print(f"async sleep end {time.strftime('%H:%M:%S')}")


async def main():
    tasks = []
    tasks.append(sleep_normal())
    tasks.append(sleep_async())
    await asyncio.gather(*tasks)
    # tasks.append(asyncio.create_task(sleep_normal()))
    # tasks.append(asyncio.create_task(sleep_async()))
    # for task in tasks:
    #     await task


if __name__ == '__main__':
    asyncio.run(main())
