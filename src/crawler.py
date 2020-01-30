import os
import time

from selenium import webdriver
from selenium.webdriver.chrome import webdriver as chrome_webdriver
from selenium.webdriver.support.select import Select
from datetime import datetime


DEBUG = True

KOSPI = (3, 'kospi')
KOSDAQ = (5, 'kosdaq')

INSTITUTION_FILE_NAME = 'institution.csv'
FOREIGNER_FILE_NAME = 'foreigner.csv'


def crawling_stock_info():
    if not DEBUG:
        options = chrome_webdriver.Options()
        download_path = '/tmp/ssad_info_{}'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
        options.add_experimental_option('prefs', {'download.default_directory': download_path})

        chrome_driver = webdriver.Chrome('../etc/chromedriver', options=options)

        chrome_driver.get('http://marketdata.krx.co.kr/contents/MKD/04/0404/04040400/MKD04040400.jsp')
        
        # change select date to today
        schdate = chrome_driver.find_element_by_name('schdate')
        schdate.clear()
        #schdate.send_keys(datetime.now().strftime('%Y%m%d'))
        schdate.send_keys(datetime.now().strftime('20200130'))

        stock_info_file_path_list = []
        for market in (KOSPI, KOSDAQ):
            # select market, KOSPI or KOSDAQ
            chrome_driver.find_element_by_css_selector(f'.design-fieldset > form > dl > dd > input:nth-child({market[0]})').click()

            select_element_id = chrome_driver.find_element_by_name('var_invr_cd').get_attribute("id")
            # 기관 합계
            invester = Select(chrome_driver.find_element_by_id(select_element_id))
            invester.select_by_value('7050')

            chrome_driver.find_element_by_class_name('btn-board.btn-board-search').click()
            excel_button = chrome_driver.find_element_by_xpath("//*[contains(text(), 'CSV')]")
            excel_button.click()

            time.sleep(6)
            institution_file_path = f'{download_path}/{market[1]}_{INSTITUTION_FILE_NAME}'
            os.rename(f'{download_path}/data.csv', institution_file_path)
            stock_info_file_path_list.append(institution_file_path)

            # 외국
            invester.select_by_value('9000')
            chrome_driver.find_element_by_class_name('btn-board.btn-board-search').click()
            excel_button.click()

            time.sleep(6)
            foreigner_file_path = f'{download_path}/{market[1]}_{FOREIGNER_FILE_NAME}'
            os.rename(f'{download_path}/data.csv', foreigner_file_path)
            stock_info_file_path_list.append(foreigner_file_path)

        chrome_driver.close()
    else:
        # excel file read
        download_path = './tests/ssad_info_2020_01_31_00_18_49'
        stock_info_file_path_list = [
            '{download_path}/kospi_institution.csv',
            '{download_path}/kospi_foreigner.csv',
            '{download_path}/kosdaq_institution.csv',
            '{download_path}/kosdaq_foreigner.csv',
        ]

    return stock_info_file_path_list


if __name__ == '__main__':
    stock_info_file_path_list = crawling_stock_info()
    print(stock_info_file_path_list)
