import os
import socket
import shutil

def main(company_path):
    output_path = os.path.join(
        os.path.dirname(company_path), f'{os.path.basename(company_path)}-attripic'
    )
    for product in os.listdir(company_path):
        product_path = os.path.join(company_path, product)
        if os.path.isdir(product_path):
            attripic_path = os.path.join(
                product_path, 'attripic'
            )
            output_single_attripic_path = os.path.join(
                output_path, product, 'attripic'
            )
            if os.path.exists(attripic_path):
                shutil.copytree(attripic_path, output_single_attripic_path)

if __name__ == '__main__':
    input_company_path = r'/Users/guoliang/Data/万圣节2-translated-translated-CHECKED-watermark/义乌市永奇服装厂-watermark'
    main(input_company_path)
