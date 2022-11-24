import os.path
import shutil

import pandas as pd
import numpy as np
OUT_DIR = r'/Users/guoliang/PycharmProjects/Script/lianzi-output'
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)


def apply_(x):
    try:
        # print(len(pd.notna(x['Variant Image'])))
        gap_position = np.sum(pd.notna(x['Variant Image']))
        x['Image Position'].iloc[0] = gap_position + 1
        x['Image Position'].iloc[gap_position] = 1
    except:
        print(x)
    return x


def convert_singel_csv(file_path):
    base_name = os.path.basename(file_path)
    data = pd.read_csv(file_path)
    group_data = data.groupby('Handle')
    new_data = group_data.apply(apply_)
    output_csv_file_path = os.path.join(OUT_DIR, base_name)
    new_data.to_csv(output_csv_file_path, index=False)


if __name__ == '__main__':
    input_path = r'/Users/guoliang/PycharmProjects/Script/lianzi'
    for item in os.listdir(input_path):
        item_path = os.path.join(input_path, item)
        if item.endswith('.csv'):
            print(item_path)
            convert_singel_csv(item_path)
