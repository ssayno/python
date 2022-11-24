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
    tasks = []
    for i in range(3):
        tasks.append(
            asyncio.create_task(print_msg(msgs[i], i+5))
        )

    for task in tasks:
        result = await task
        # print(f"Sleep {result} seconds done  at {time.strftime('%H:%M:%S')}")
    print(f"End time: {time.strftime('%H:%M:%S')}")


asyncio.run(main())
