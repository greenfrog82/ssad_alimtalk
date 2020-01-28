import json
import os
import requests

from stock import get_stock_info

SLACK_INCOMMING_WEBHOOK_URL = 'https://hooks.slack.com/services/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'


def change_working_directory():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


if __name__ == '__main__':
    change_working_directory()

    _, stock_info = get_stock_info()
    print('-----')
    print(stock_info)

    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'text': stock_info,
    }

    response = requests.post(SLACK_INCOMMING_WEBHOOK_URL, data=json.dumps(data), headers=headers)
    print(response)
