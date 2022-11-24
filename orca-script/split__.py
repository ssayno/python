#!/usr/bin/env python3
import fileinput
import os
import csv


def single_(file_path):
    global new_
    new_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding='U8') as f:
        csv_ = csv.reader(f)
        new_.append(next(csv_))
        for row in csv_:
            if row[17] != "":
                row[17] = row[17].split('.')[0] + '.99'
                row[18] = row[18].split('.')[0] + '.99'
            new_.append(row)
    with open(f'{new_name}-fin.csv', 'w+', encoding='U8') as f:
        csv__ = csv.writer(f)
        csv__.writerows(new_)

if __name__ == '__main__':
    input_path = r'csv'
    for file_ in os.listdir(input_path):
        csv_file_path = os.path.normpath(os.path.join(input_path, file_))
        multiple_dict = {}
        new_= []
        if file_.endswith('.csv'):
            single_(csv_file_path)
