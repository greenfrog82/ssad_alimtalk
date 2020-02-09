#-*- coding:utf-8 -*-
import csv
import os
from collections import OrderedDict
from datetime import date

from crawler import crawling_stock_info


def _parse_simple_stock_info(stock_info_file_path):
    dict_stock_info = {}
    csv_read = csv.reader(open(stock_info_file_path, 'r'))

    first_row = True
    for row in csv_read:
        if first_row:
            first_row = False
            continue
        temp = {'name': row[1], 'purchase_amount': float(row[7].replace(",", ""))}
        dict_stock_info[row[0]] = temp

    return dict_stock_info 

def parse_stock_info(stock_info_file_path, stock_info_msg_title):
    dict_public_office = _parse_simple_stock_info(stock_info_file_path)
    stock_info_msg = ''

    stock_info_msg += f'{stock_info_msg_title} TOP 5\n'
    sorted_public_office = OrderedDict(sorted(dict_public_office.items(), reverse=True, key=lambda x: (x[1]['purchase_amount'])))

    count = 1
    for key, values in sorted_public_office.items():
        if count > 5:
            break
        stock_info_msg += f"{count}. {values['name']}\n"
        count+=1

    return stock_info_msg, sorted_public_office

def get_double_buying_companies(foreigner_stock_info, public_office_stock_info, state_pension_stock_info):
    total_stock_info_msg = ''
    foreigner_stock_info_list = list(foreigner_stock_info.items())[:50]
    public_office_stock_info_list = list(public_office_stock_info.items())[:50]

    count = 1
    for p_item in public_office_stock_info_list:
        for f_item in foreigner_stock_info_list:
            if p_item[0] == f_item[0] and p_item[0] in state_pension_stock_info and state_pension_stock_info[p_item[0]]['purchase_amount'] > 0:
                total_stock_info_msg += f"{count}. {p_item[1]['name']}\n"
                count += 1
                break

    return total_stock_info_msg 

# TODO: need refactoring get_stock_info function. 
# first of all, pytest has to introduce to write test codes.
def get_stock_info():
    stock_info_file_path_list = crawling_stock_info()

    today = date.today()
    stock_info_msg = f'{today.year}년 {today.month}월 {today.day}일 시간외 외인/기관 순매수 TOP 5 알림!!\n\n'

    foreigner_stock_info_msg, foreigner_stock_info = parse_stock_info(stock_info_file_path_list[2], '외인')
    public_office_stock_info_msg, public_office_stock_info = parse_stock_info(stock_info_file_path_list[0], '기관')

    stock_info_msg += '-- 코스피 --\n\n'
    stock_info_msg += foreigner_stock_info_msg
    stock_info_msg += '\n'
    stock_info_msg += public_office_stock_info_msg

    stock_info_msg += '\n'
    stock_info_msg += '50위권내의 양매수\n'
    stock_info_msg += get_double_buying_companies(foreigner_stock_info, public_office_stock_info, _parse_simple_stock_info(stock_info_file_path_list[1]))

    foreigner_stock_info_msg, foreigner_stock_info = parse_stock_info(stock_info_file_path_list[5], '외인')
    public_office_stock_info_msg, public_office_stock_info = parse_stock_info(stock_info_file_path_list[3], '기관')

    stock_info_msg += '\n'
    stock_info_msg += '-- 코스닥 --\n\n'
    stock_info_msg += foreigner_stock_info_msg
    stock_info_msg += '\n'
    stock_info_msg += public_office_stock_info_msg
    stock_info_msg += '\n'
    stock_info_msg += '50위권내의 양매수\n'
    stock_info_msg += get_double_buying_companies(foreigner_stock_info, public_office_stock_info, _parse_simple_stock_info(stock_info_file_path_list[4]))

    return stock_info_msg 


if __name__ == '__main__':
    stock_info_msg = get_stock_info()
    print(stock_info_msg)
