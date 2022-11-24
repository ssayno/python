import math
import os
import random
import shutil


def main(company_path, n=4):
    if not os.path.exists(company_path):
        print('输入正确的路径')
        return
    # directory
    dirs = []
    for i in range(n):
        tmp_dir = os.path.join(
            os.path.dirname(company_path), f'{os.path.basename(company_path)}-{i+1}'
        )
        # 确定
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        dirs.append(tmp_dir)
    all_products = []
    for single_product in os.listdir(company_path):
        single_product_path = os.path.join(company_path, single_product)
        if os.path.isdir(single_product_path):
            all_products.append(single_product_path)
    random.shuffle(all_products)
    samples = math.ceil(len(all_products) / n)
    count_ = 0
    while count_ < n - 1:
        need_move_dirs = all_products[count_ * samples: (count_ + 1) * samples]
        for need_move_dir in need_move_dirs:
            shutil.move(need_move_dir, dirs[count_])
        count_ += 1
    #
    for need_move_dir in all_products[count_ * samples: (count_ + 1) * samples]:
        shutil.move(need_move_dir, dirs[count_])


if __name__ == '__main__':
    input_company_path = r'/Users/guoliang/Data/test_/保定美港箱包制造有限公司'
    main(input_company_path)
