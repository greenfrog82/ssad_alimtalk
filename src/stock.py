#-*- coding:utf-8 -*-
import csv
import os
import time
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.chrome import webdriver as chrome_webdriver
from selenium.webdriver.support.select import Select
from datetime import datetime

DEBUG = False


# TODO: need refactoring get_stock_info function. 
# first of all, pytest has to introduce to write test codes.
def get_stock_info():
    if not DEBUG:
        options = chrome_webdriver.Options()
        download_path = '/tmp/ssad_info_{}'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
        options.add_experimental_option('prefs', {'download.default_directory': download_path})

        chrome_driver = webdriver.Chrome('../etc/chromedriver', options=options)

        chrome_driver.get('http://marketdata.krx.co.kr/contents/MKD/04/0404/04040400/MKD04040400.jsp')

        select_element_id = chrome_driver.find_element_by_name('var_invr_cd').get_attribute("id")
        # 기관 합계
        invester = Select(chrome_driver.find_element_by_id(select_element_id))
        invester.select_by_value('7050')

        chrome_driver.find_element_by_class_name('btn-board.btn-board-search').click()
        excel_button = chrome_driver.find_element_by_xpath("//*[contains(text(), 'CSV')]")
        excel_button.click()

        time.sleep(6)

        # 외국
        invester.select_by_value('9000')
        chrome_driver.find_element_by_class_name('btn-board.btn-board-search').click()
        excel_button.click()

        time.sleep(6)

        chrome_driver.close()
    else:
        # excel file read
        download_path = '/tmp/ssad_info_2020_01_28_19_41_00'

    file_list = os.listdir(download_path)

    # 기관 자료 read
    dict_public_office = {}
    file_public_office = open('{}/{}'.format(download_path, file_list[0]), 'r')
    csv_read = csv.reader(file_public_office)

    first_row = True
    for row in csv_read:
        if first_row:
            first_row = False
            continue
        temp = {'name': row[1], 'purchase_amount': float(row[7].replace(",", ""))}
        dict_public_office[row[0]] = temp

    # 기관 자료 sort
    print('기관 TOP 5')
    sorted_public_office = OrderedDict(sorted(dict_public_office.items(), reverse=True, key=lambda x: (x[1]['purchase_amount'])))

    top_public_office = {}
    count = 0
    for key, values in sorted_public_office.items():
        if count > 4:
            break
        print('{} {} {}'.format(key, values['name'], values['purchase_amount']))
        top_public_office[count] = {'code': key, 'name': values['name'], 'purchase_amount': values['purchase_amount']}
        count+=1

    # 외국인 자료 read
    file_foreigner = open('{}/{}'.format(download_path, file_list[1]), 'r')
    csv_read = csv.reader(file_foreigner)

    dict_foreigner_office = {}
    first_row = True
    for row in csv_read:
        if first_row:
            first_row = False
            continue
        temp = {'name': row[1], 'purchase_amount': float(row[7].replace(",", ""))}
        dict_foreigner_office[row[0]] = temp

    # 외국인 자료 sort
    sorted_foreigner_office = OrderedDict(sorted(dict_foreigner_office.items(), reverse=True, key=lambda x: (x[1]['purchase_amount'])))

    print('')
    print('외국인 TOP 5')
    top_foreigner_office = {}
    count = 0
    for key, values in sorted_foreigner_office.items():
        if count > 4:
            break
        print('{} {} {}'.format(key, values['name'], values['purchase_amount']))
        top_foreigner_office[count] = {'code': key, 'name': values['name'], 'purchase_amount': values['purchase_amount']}
        count+=1

    # TODO: fix the following codes which does not work properly.
    intersection_codes = set(dict_public_office).intersection(set(dict_foreigner_office))
    dict_intersection = {}
    for code in intersection_codes:
        dict_intersection[code] = {'name': dict_public_office[code]['name'], 'purchase_amount': dict_public_office[code]['purchase_amount']}

    sorted_intersection = OrderedDict(sorted(dict_intersection.items(), reverse=True, key=lambda x: (x[1]['purchase_amount'])))
    dict_stock_info = {}
    stock_info_msg = ''
    count = 0
    
    print('')
    print('기관/외국인 양매수 TOP 5')
    for key, values in sorted_intersection.items():
        if count > 4:
            break
        stock_info = '{} {} {}'.format(key, values['name'], values['purchase_amount'])
        print(stock_info)
        
        stock_info_msg += f'{stock_info}\n'
        dict_stock_info[count] = {'code': key, 'name': values['name'], 'purchase_amount': values['purchase_amount']}
        count+=1
    
    return dict_stock_info, stock_info_msg


if __name__ == '__main__':
    dict_stock_info, stock_info_msg = get_stock_info()