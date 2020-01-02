from flask import Flask, escape, request, render_template
import requests
import json
import os

KAKAO_REST_API_KEY = os.environ['KAKAO_REST_API_KEY']

app = Flask(__name__)

access_token = None
refresh_token = None

@app.route('/')
def index():
    return render_template('index.html', kakao_rest_api_key=KAKAO_REST_API_KEY)

@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    response = get_access_token(KAKAO_REST_API_KEY, str(code))
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')

    response = send_message(access_token)
    print(response)
    return f'code={code}<br />access_token={access_token}<br />refresh_token={refresh_token}'

def get_access_token(clientId, code):      
    url = 'https://kauth.kakao.com/oauth/token'
    payload = f'grant_type=authorization_code&client_id={clientId}&redirect_url=http%3A%2F%2Flocalhost%3A5000%2Foauth&code={code}'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(((response.text).encode('utf-8')))

def send_message(access_token):
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    payload = {
        "object_type": "text",
        "text": "test",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
    }
    payload = json.dumps(payload)
    payload = f'template_object={payload}'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(((response.text).encode('utf-8')))

@app.route('/hello')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


if __name__ == '__main__':
    # app.run(debug=True)
    response = send_message('mxtiVCCSlfyxXwa-rIev9GgMqBGFH9USbpBrWgorDNMAAAFvaHU3Xw')
    print(response)
