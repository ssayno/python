#!/usr/bin/env python3
import re
import pandas as pd


def read_titles_from_csv(csv_path):
    data = pd.read_csv(csv_path)
    titles = data['Title']
    data.groupby('Handle').apply(handle_title).to_csv('orcajump-after-regexp.csv')
    all_titles = titles[pd.notna(titles)]
    return all_titles.values

def handle_title(x):
    title = x['Title'].iloc[0]
    patten = re.compile(r'(?:\d{1,3}(?:[,/.]\d{0,3})?\s?[*xX]?\s?){2,}(?:cm|pcs|CM|PCS)(?:\s?[*xX]\s?\d{1,3}(?:PCS|pcs))?')
    match_result = patten.findall(title)
    if match_result != []:
        for mr in match_result:
            if re.search('[.*xX]', mr):
                x['Title'].iloc[0] = title.replace(mr, "")
    return x




def remove_other_infos_from_titles(csv_path):
    titles = read_titles_from_csv(csv_path)
    if titles is None:
        return
    after_titles = []
    star_titls = []
    patten = re.compile(r'(?:\d{1,3}(?:[,/.]\d{0,3})?\s?[*xX]?\s?){2,}(?:cm|pcs|CM|PCS)(?:\s?[*xX]\s?\d{1,3}(?:PCS|pcs))?')
    count = 0
    start_count = 0
    for title in titles:
        match_result = patten.findall(title)
        if '*' in title or 'X' in title or 'x' in title:
            start_count += 1
            star_titls.append(title)
        if match_result != []:
            count += 1
            for mr in match_result:
                print(mr, title)
                if re.search('[.*xX]', mr):
                    after_titles.append(title.replace(mr, ""))
            #print(match_result, title)
    print(f'匹配到 {count} 个，有星号的 {start_count}')
    with open('star_titles.txt', 'w+', encoding='U8') as f:
        f.write('\n'.join(star_titls))

    with open('after_titles.txt', 'w+', encoding='U8') as f:
        f.write('\n'.join(after_titles))

if __name__ == '__main__':
    csv_path = 'orcajump.csv'
    remove_other_infos_from_titles(csv_path)
