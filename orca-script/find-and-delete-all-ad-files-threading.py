#!/usr/bin/env python3
import asyncio
import os
import threading
import glob
import imagesize
from PIL import Image
import concurrent.futures
"""
input area
"""
# var
DIEECTORY = r'D:\D-Desktops\testtt_'
# image blacklist directory
BLACKLIST_DIETOYR = r'D:\D-Desktops\黑名单'
# need delete pic info list
blacklist_info_list = []
# need delete pic list, ???????? no
delete_file_list = []
# verify?
verify_img = True


def _get_blacklist_image_and_dimension():
    global blacklist_info_list
    jpg_list = glob.glob(BLACKLIST_DIETOYR + '/**/*.jpg', recursive=True)
    for path in jpg_list:
        file_size = os.path.getsize(path)
        width, height = imagesize.get(path)
        blacklist_info_list.append((width, height, file_size))

def _should_delete(width, height, filesize):
    if width < 400 or height < 400:
        return True
    if width < 1 or height < 1:
        return True
    ratio = width / height
    if ratio < 0.25 or ratio > 4:
        return False
    if len(blacklist_info_list) == 0:
        return False

    if (width, height, filesize) in blacklist_info_list:
        print((width, height, filesize), blacklist_info_list)
        return True
    return False

class Single_Directory_Run(threading.Thread):
    def __init__(self, single_dir_path) -> None:
        super(Single_Directory_Run, self).__init__()
        self.sdp = single_dir_path

    def run(self):
        asyncio.run(self.main())

    async def main(self):
        target_command = []
        for product in os.listdir(self.sdp):
            product_path = os.path.join(self.sdp, product)
            if product.startswith('.') or not os.path.isdir(product_path):
                continue
            target_command.append(
                self.run_single_product_dir(product_path=product_path)
            )
        await asyncio.gather(*target_command)

    async def run_single_product_dir(self, product_path):
        # extract all pic
        for item in os.listdir(product_path):
            item_path = os.path.join(product_path, item)
            if not os.path.isdir(item_path) or item.startswith('.'):
                continue
            for pic in os.listdir(item_path):
                pic_path = os.path.join(item_path, pic)
                if pic.startswith('.') or not os.path.isfile(pic_path):
                    continue
                try:
                    img = Image.open(pic_path)
                    if verify_img:
                        img.verify()
                except (IOError, SyntaxError):
                    delete_file_list.append(pic_path)
                    continue
                width, height = imagesize.get(pic_path)
                filesize = os.path.getsize(pic_path)
                if _should_delete(width, height, filesize):
                    delete_file_list.append(pic_path)
                    os.remove(pic_path)


if __name__ == '__main__':
    # get blacklist info
    _get_blacklist_image_and_dimension()
    print(f'blacklist info load finished {blacklist_info_list}')
    for dir_item in os.listdir(DIEECTORY):
        dir_item_path = os.path.join(DIEECTORY, dir_item)
        if dir_item.startswith('.') or not os.path.isdir(dir_item_path):
            continue
        temp_threading_obj = Single_Directory_Run(dir_item_path)
        temp_threading_obj.start()
