import os
import time

from selenium import webdriver
from selenium.webdriver.chrome import webdriver as chrome_webdriver
from selenium.webdriver.support.select import Select
from datetime import datetime

from settings import DEBUG


KOSPI = (3, 'kospi')
KOSDAQ = (5, 'kosdaq')

INSTITUTION_FILE_NAME = 'institution.csv'
STATE_PENSION_FILE_NAME = 'state_pension.csv'
FOREIGNER_FILE_NAME = 'foreigner.csv'

INSTITUION_INVESTER_CODE = '7050'
STATE_PENSION_INVESTOR_CODE = '6000'
FOREIGNER_INVESTER_CODE = '9000'


def _parse_stock_information_by_class(chrome_driver, invester_element, invester_code, market, download_path, data_file_name, wait_for_sleep=6):
    invester_element.select_by_value(invester_code)

    chrome_driver.find_element_by_class_name('btn-board.btn-board-search').click()
    excel_button = chrome_driver.find_element_by_xpath("//*[contains(text(), 'CSV')]")
    excel_button.click()

    time.sleep(wait_for_sleep)
    file_path = f'{download_path}/{market[1]}_{data_file_name}'
    os.rename(f'{download_path}/data.csv', file_path)

    return file_path

def crawling_stock_info():
    options = chrome_webdriver.Options()
    download_path = '/tmp/ssad_info_{}'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    options.add_experimental_option('prefs', {'download.default_directory': download_path})

    chrome_driver = webdriver.Chrome('../etc/chromedriver', options=options)

    chrome_driver.get('http://marketdata.krx.co.kr/contents/MKD/04/0404/04040400/MKD04040400.jsp')
    
    # change select date to today
    schdate = chrome_driver.find_element_by_name('schdate')
    schdate.clear()
    schdate.send_keys(datetime.now().strftime('%Y%m%d'))
    # schdate.send_keys(datetime.now().strftime('20200207'))

    stock_info_file_path_list = []
    for market in (KOSPI, KOSDAQ):
        # select market, KOSPI or KOSDAQ
        chrome_driver.find_element_by_css_selector(f'.design-fieldset > form > dl > dd > input:nth-child({market[0]})').click()

        select_element_id = chrome_driver.find_element_by_name('var_invr_cd').get_attribute("id")
        invester_element = Select(chrome_driver.find_element_by_id(select_element_id))
        # 기관 합계
        stock_info_file_path_list.append(_parse_stock_information_by_class(chrome_driver, invester_element, INSTITUION_INVESTER_CODE, market, download_path, INSTITUTION_FILE_NAME))
        # 연기금
        stock_info_file_path_list.append(_parse_stock_information_by_class(chrome_driver, invester_element, STATE_PENSION_INVESTOR_CODE, market, download_path, STATE_PENSION_FILE_NAME))
        # 외국
        stock_info_file_path_list.append(_parse_stock_information_by_class(chrome_driver, invester_element, FOREIGNER_INVESTER_CODE, market, download_path, FOREIGNER_FILE_NAME))

    chrome_driver.close()
    return stock_info_file_path_list


if __name__ == '__main__':
    stock_info_file_path_list = crawling_stock_info()
    print(stock_info_file_path_list)
