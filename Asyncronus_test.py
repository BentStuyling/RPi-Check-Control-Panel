#!/usr/bin/env python3
# countasync.py

import asyncio, time
import random

templist =[0]*10

async def coolant():
    n =1
    while True:
        value = round(random.uniform(0,80)/10,1)
        templist.append(value)
        del templist[0]
        await asyncio.sleep(1)
        n = n +1
        print('coolant', value)
        if n == 10:
            print('coolant', time.perf_counter() - s)

async def oil():
    n =1
    while True:
        value = round(random.uniform(0,80)/10,1)
        templist.append(value)
        del templist[0]
        await asyncio.sleep(1)
        n = n +1
        print ('oil', value)
        if n == 10:
            print('oil temp', time.perf_counter() - s)

async def main():
    asyncio.gather(coolant(), oil())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    print('coolant startet')
    
    print('oil started')
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")