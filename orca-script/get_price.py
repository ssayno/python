import json
import os
import matplotlib
import matplotlib.pyplot as plt
import asyncio
from operator import itemgetter




input_path = r'D:\D-Desktops\Datas-Directory\身体链-11-15\10-28身体链子做表\CHECKED\YWSJJMYSH'
matplotlib.rc("font",family='MicroSoft YaHei',weight="bold")

results = {}


async def read_price(price_file_path):
    global result
    with open(price_file_path, 'rb') as f:
        json_data = json.load(f)
        await asyncio.sleep(0)
        price = float(json_data['scale_price'].split('-')[0].strip('￥'))
        if price in results:
            results[price] += 1
        else:
            results[price] = 1




async def main(input_path):
    tasks = []
    for sku in os.listdir(input_path):
        if sku.startswith('.'):
            continue
        sku_path = os.path.join(input_path, sku)
        if not os.path.isdir(sku_path):
            continue
        price_file_path = os.path.join(sku_path, 'prices.json')
        if os.path.exists(price_file_path):
            tasks.append(read_price(price_file_path))
        else:
            print(f'{sku} 没有 price')
    await asyncio.gather(*tasks)




if __name__ == '__main__':
    asyncio.run(main(input_path=input_path))
    sorted_result = {k: v for k, v in sorted(results.items(), key=itemgetter(0), reverse=True)}
    print(sorted_result)
    fig = plt.figure()
    plt.title(os.path.basename(input_path) + " 进价图")
    plt.plot(sorted_result.keys(), sorted_result.values())
    plt.xlabel('Price')
    plt.ylabel('Count')
    plt.savefig('result.jpg')
    plt.show()
