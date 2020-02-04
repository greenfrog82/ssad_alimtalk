import json
import os
import requests

from stock import get_stock_info

SLACK_INCOMMING_WEBHOOK_URL = os.environ['SLACK_INCOMING_HOOK']

# https://stackoverflow.com/questions/1432924/python-change-the-scripts-working-directory-to-the-scripts-own-directory
def change_working_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


if __name__ == '__main__':
    change_working_directory()

    stock_info = get_stock_info()
    print(stock_info)

    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'text': stock_info,
    }

    response = requests.post(SLACK_INCOMMING_WEBHOOK_URL, data=json.dumps(data), headers=headers)
    print(response)
