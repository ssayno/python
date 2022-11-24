import concurrent.futures
import json
import os
import re
import shutil
import deepl

# baidu
APP_ID = ''  # 你的appid
SECRET_KEY = ''  # 你的密钥
# youdao
APP_KEY = ''  # 应用ID
APP_SECRET = ''  # 应用秘钥
# deepl
DEEPL_AUTH_KEY = '4b813c8a-d166-2dd2-1e71-ae0506b1a26b'  # YOUR_AUTH_KEY


class Deepl_Translator:
    def __init__(self):
        """
        deepl 的连接是一次建立多次使用
        安装: pip install deepl
        """
        self.translator = deepl.Translator(DEEPL_AUTH_KEY)

    def deepl_translate_normal(self, query_text, from_lang, to_lang):
        after_translated_text = self.translator.translate_text(query_text, source_lang=from_lang,
                                                               target_lang=to_lang).text
        return after_translated_text.strip()


def translate_attribute_pic(product_path):
    global cache_dict, output_path
    if not os.path.isdir(product_path):
        print(product_path)
        return False
    product_attripic_path = os.path.join(
        product_path, 'attripic'
    )
    if not os.path.exists(product_attripic_path):
        print(f'{product_path} 没有 attripic')
        shutil.rmtree(product_path)
        return False
    for single_attripic in os.listdir(product_attripic_path):
        temp_ = single_attripic.split('.')
        prefix = '-'.join(temp_[:-1])
        suffix = temp_[-1]
        need_translate_name = re.sub(
            '[-]{2,}', '-', re.sub(
                '[+]', '&',
                re.sub(
                    '[,，。【】（）*]|[\x21-\x2a]', '', prefix
                )
            )
        )
        single_attripic_path = os.path.join(product_attripic_path, single_attripic)
        if cache_dict.get(single_attripic, None) is None:
            translate_result = Deepl_Translator().deepl_translate_normal(need_translate_name, from_lang='ZH',
                                                                         to_lang='EN-US')
            value = f'{translate_result}.{suffix}'
            cache_dict[single_attripic] = value
            new_single_attripic_path = os.path.join(product_path, value)
            os.replace(single_attripic_path, new_single_attripic_path)
    else:
        shutil.copy(product_attripic_path, output_path)


if __name__ == '__main__':
    # single_attripic = 'flajfk----asfkjj+flka.afjs.jpg'
    # need_translate_name = re.sub(
    #     '[-]{2,}', '-', re.sub(
    #         '[+]', '&',
    #         re.sub(
    #             '[,，。【】（）*]|[\x21-\x2a]', '', '-'.join(single_attripic.split('.')[:-1])
    #         )
    #     )
    # )
    # print(need_translate_name)
    cache_dict = {}
    input_path = r''
    output_path = os.path.join(
        os.path.dirname(input_path), f'{os.path.basename(input_path)}-attripic'
    )
    single_products = []
    for item in os.listdir(input_path):
        item_path = os.path.normpath(
            os.path.join(input_path, item)
        )
        if os.path.isdir(item_path):
            single_products.append(item_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(translate_attribute_pic, single_products)

    with open('title-cache.json', 'a+', encoding='U8') as f:
        json.dump(cache_dict, f, indent='\t', ensure_ascii=False)