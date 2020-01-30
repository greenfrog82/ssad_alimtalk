#-*- coding:utf-8 -*-
import csv
import os
from collections import OrderedDict

from crawler import crawling_stock_info

def parse_stock_info(stock_info_file_path, stock_info_msg_title):
    dict_public_office = {}
    file_public_office = open(stock_info_file_path, 'r')
    csv_read = csv.reader(file_public_office)

    first_row = True
    for row in csv_read:
        if first_row:
            first_row = False
            continue
        temp = {'name': row[1], 'purchase_amount': float(row[7].replace(",", ""))}
        dict_public_office[row[0]] = temp

    stock_info_msg = ''

    # 기관 자료 sort
    stock_info_msg += f'{stock_info_msg_title} TOP 5\n'
    sorted_public_office = OrderedDict(sorted(dict_public_office.items(), reverse=True, key=lambda x: (x[1]['purchase_amount'])))

    top_public_office = {}
    count = 1
    for key, values in sorted_public_office.items():
        if count > 5:
            break
        stock_info_msg += '{} {}\n'.format(count, values['name'])
        top_public_office[count] = {'code': key, 'name': values['name'], 'purchase_amount': values['purchase_amount']}
        count+=1

    return stock_info_msg


# TODO: need refactoring get_stock_info function. 
# first of all, pytest has to introduce to write test codes.
def get_stock_info():
    stock_info_file_path_list = crawling_stock_info()

    stock_info_msg = '-- 코스피 --\n\n'
    stock_info_msg += parse_stock_info(stock_info_file_path_list[0], '기관')
    stock_info_msg += '\n'
    stock_info_msg += parse_stock_info(stock_info_file_path_list[1], '외인')

    stock_info_msg += '\n'
    stock_info_msg += '-- 코스닥 --\n\n'
    stock_info_msg += parse_stock_info(stock_info_file_path_list[2], '기관')
    stock_info_msg += '\n'
    stock_info_msg += parse_stock_info(stock_info_file_path_list[3], '외인')

    return stock_info_msg 


if __name__ == '__main__':
    stock_info_msg = get_stock_info()
    print(stock_info_msg)
