import asyncio

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
        # print([(item.name, item.code) for item in self.translator.get_source_languages()])

    async def deepl_translate(self, query_text, from_lang, to_lang):
        after_translated_text = self.translator.translate_text(query_text, source_lang=from_lang,
                                                               target_lang=to_lang).text
        print(after_translated_text.strip())
        return after_translated_text.strip()

    def deepl_translate_normal(self, query_text, from_lang, to_lang):
        after_translated_text = self.translator.translate_text(query_text, source_lang=from_lang,
                                                               target_lang=to_lang).text
        print(after_translated_text.strip())
        return after_translated_text.strip()

async def main():
    translate = Deepl_Translator()
    need_translate_text = [
        '这是什么',
        '这个好玩',
        '算了不想玩了'
    ]
    target_task = [
        translate.deepl_translate(item, 'ZH', 'EN-US') for item in need_translate_text
    ]
    await asyncio.gather(*target_task)

if __name__ == '__main__':
    asyncio.run(main())
