#!/usr/bin/env python3
import pandas as pd
import os
from random import choice, randint





def deal_with_single_csv_file(file_path):
    global handle_count
    global output_path
    new_name = os.path.basename(file_path).split('.')[0]
    data = pd.read_csv(file_path)
    group_data = data.groupby('Handle')
    handle_count = len(group_data)
    print(handle_count)
    output_csv_file_path = os.path.join(output_path, f'{new_name}-new.csv')
    group_data.apply(apply_).to_csv(output_csv_file_path, index=False)


def apply_(x):
    for index_, value in enumerate(x['Variant Price']):
        if not pd.isna(value):
            if value < 20:
                multiple = 1.4
            elif value < 30:
                multiple = 1.2
            else:
                multiple = 1
            x['Variant Price'].iloc[index_] = str(
                x['Variant Price'].iloc[index_] * multiple
            ).split('.')[0] + '.99'
            x['Variant Compare At Price'].iloc[index_] = str(
                x['Variant Compare At Price'].iloc[index_] * multiple
            ).split('.')[0] + '.99'
    return x


if __name__ == '__main__':
    handle_count = 0
    input_path = r'Fisdy 改价'
    output_path = input_path + '-output'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for file_ in os.listdir(input_path):
        csv_file_path = os.path.normpath(os.path.join(input_path, file_))
        multiplied_dict = {}
        if file_.startswith('.'):
            continue
        if file_.endswith('.csv'):
            deal_with_single_csv_file(csv_file_path)
