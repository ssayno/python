#!/usr/bin/env python3
import asyncio
import time


async def print_msg(msg, seconds):
    print(f"{msg} start, sleep {seconds} seconds at {time.strftime('%H:%M:%S')}")
    await asyncio.sleep(seconds)
    print(f"{msg} end, afte sleep {seconds} seconds at {time.strftime('%H:%M:%S')}")
    return seconds

async def main():
    print(f"Start time: {time.strftime('%H:%M:%S')}")
    msgs = ["First", "Second", "Third"]
    for i in range(3):
        result = await print_msg(msgs[i], i + 2)
        print(f'Seconds is ===> {result} done at {time.strftime("%H:%M:%S")}')
    print(f"End time: {time.strftime('%H:%M:%S')}")


asyncio.run(main())
