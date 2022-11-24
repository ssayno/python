#!/usr/bin/env python3
import os
import re


def convert_string_to_standrad(name: str):
    return re.sub(
        '-{2,}', '-', re.sub(
            '[& ]', '-', name
        )
    )


def path_replace(name, parent_path):
    if name.startswith('.'):
        return False
    origin_path = os.path.join(parent_path, name)
    if not os.path.isdir(origin_path):
        return False
    new_name = convert_string_to_standrad(name)
    new_path = os.path.join(parent_path, new_name)
    # os.replace(origin_path, new_path)
    return new_path


def convert_shiying(shiying_sku_path):
    for main_category in os.listdir(shiying_sku_path):
        print(main_category)
        new_mc_path = path_replace(main_category, shiying_sku_path)
        if not new_mc_path:
            continue
        for sub_category in os.listdir(new_mc_path):
            print(sub_category)
            new_sc_path = path_replace(sub_category, new_mc_path)



if __name__ == '__main__':
    convert_shiying(r'/Users/guoliang/Data/SKU')
