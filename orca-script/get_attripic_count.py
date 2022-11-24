import os


def count_attripic(path):
    global all_count, attripic_count
    for item in os.listdir(path):
        item_path = os.path.join(
            path, item
        )
        if os.path.isdir(item_path):
            attripic_path = os.path.join(
                item_path, 'attripic'
            )
            all_count += 1
            if os.path.exists(attripic_path):
                attripic_count += 1


if __name__ == '__main__':
    all_count = 0
    attripic_count = 0
    input_path = r'/Users/guoliang/Data/万圣节2-translated-translated-CHECKED-watermark/义乌市春谦服饰有限公司-watermark'
    count_attripic(input_path)
    print(f'总的数量为 {all_count}, 有 attripic 的数量为 {attripic_count}')