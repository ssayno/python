import os


def extract_(company_path, txt_file_path):
    single_volume = company_path.split(os.sep)
    with open(txt_file_path, 'r', encoding='U8') as f:
        need_concat_images_path = [
            item.strip().split('\\') for item in f.readlines()
        ]
    print(need_concat_images_path)
    print(single_volume)


if __name__ == '__main__':
    input_company_path = r'/Users/guoliang/PycharmProjects/pyqt5/src/UI_files'
    txt_file_path = ''
    extract_(input_company_path)
