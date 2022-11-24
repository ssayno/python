#!/usr/bin/env python3
import os
import glob


input_path = r''
describe_txts = glob.glob(input_path + '/**/*.descript.txt', recursive=True)
skus = []
for des in describe_txts:
    sku = os.path.split(os.sep)[-2]
    print(sku)
    skus.append(sku)
    break
with open('skus.txt', 'w+', encoding='utf8') as f:
    f.write(os.linesep.join(skus))
