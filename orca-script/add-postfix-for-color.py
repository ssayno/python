#!/usr/bin/env python3
import pandas as pd


def apply_(x):
    pass

def apply_(x):
    color_groupby_data = x.groupby('Option1 Value')
    origin_color_option = x['Option1 Value'][pd.notna(x['Option1 Value'])].unique()
    origin_color_length = len(origin_color_option)
    groupby_color_length = len(color_groupby_data)
    count = set()
    for _, item in color_groupby_data:
        # print(_, item['Option1 Value'].unique())
        count.add(item['Option1 Value'].unique()[0])
    if origin_color_length != len(count):
        print(origin_color_option)
        if groupby_color_length > 1:
            print(origin_color_length, groupby_color_length)
            print('-' * 20)


def apply_with_variant_sku(x):
    data = x['Variant SKU'][pd.notna(x['Variant SKU'])]
    variant_sku_length = len(data)
    unique_variant_sku_length = len(data.unique())
    # print(variant_sku_length, unique_variant_sku_length)
    if variant_sku_length != unique_variant_sku_length:
        print(variant_sku_length, unique_variant_sku_length)
        print(x)


def main(csv_path):
    data = pd.read_csv(csv_path)
    gropy_data = data.groupby("Handle")
    gropy_data.apply(apply_with_variant_sku)

if __name__ == '__main__':
    csv_path = r'___Concatinated-all-csv-file.csv'
    main(csv_path)
