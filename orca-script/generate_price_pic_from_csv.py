#!/usr/bin/env python3
import pandas as pd
from itertools import chain
import os
import matplotlib.pyplot as plt
import asyncio


def get_price_from_single_handle(item):
    prices = item['Variant Price']
    notna_prices = prices[prices.notna()].unique()
    # print(notna_prices, len(notna_prices))
    return notna_prices

async def get_price_from_single_csv(csv_file_path):
    data = pd.read_csv(csv_file_path, low_memory=False)
    groupyed_data = data.groupby('Handle')
    all_prices = groupyed_data.apply(get_price_from_single_handle)
    return chain.from_iterable(all_prices)


async def generate_from_dir(dir_path):
    tasks = []
    prcies_dict = {}
    for file_ in os.listdir(dir_path):
        if file_.startswith('.') or not file_.endswith('.csv'):
            continue
        csv_file_path = os.path.join(dir_path, file_)
        tasks.append(
            asyncio.create_task(get_price_from_single_csv(csv_file_path))
        )
    for task in tasks:
        prices = await task
        for price in prices:
            if price in prcies_dict:
                prcies_dict[price] += 1
            else:
                prcies_dict[price] = 1
    sorted_data = dict(sorted(prcies_dict.items(), key=lambda x: x[0]))
    x_data = sorted_data.keys()
    y_data = sorted_data.values()
    plt.xlabel("Price")
    plt.ylabel("Count")
    plt.title("Fisdy " + "Price distribute line chart")
    plt.plot(x_data, y_data)
    plt.savefig("result.jpg")


if __name__ == '__main__':
    input_path = r'Fisdy 改价'
    asyncio.run(generate_from_dir(input_path))
