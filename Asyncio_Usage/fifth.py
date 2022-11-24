#!/usr/bin/env python3
import asyncio
import time

# time.strftime('%H:%M:%S')

async def single_sleep():
    print(f'Head {time.strftime("%H:%M:%S")}')
    await asyncio.sleep(2)
    print(f'Middle {time.strftime("%H:%M:%S")}')
    await asyncio.sleep(4)
    print(f'Tail {time.strftime("%H:%M:%S")}')
    await asyncio.sleep(19)

async def main():
    await single_sleep()


if __name__ == '__main__':
    asyncio.run(main())
