from flask import Flask, render_template
import requests
import os

# Vercel이 이 'app'을 찾으려고 합니다. 절대 들여쓰기 하지 마세요!
app = Flask(__name__)

@app.route('/')
def index():
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        try:
            # 공공데이터 API 주소
            url_arr = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
            url_dep = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
            
            # 인증키가 인코딩되어 있을 경우를 대비
            service_key = requests.utils.unquote(api_key)
            
            params = {
                'serviceKey': service_key,
                'type': 'json',
                'numOfRows': '100'
            }

            res_a = requests.get(url_arr, params=params, timeout=10)
            if res_a.status_code == 200:
                data = res_a.json()
                items = data.get('response', {}).get('body', {}).get('items', [])
                arrivals = items if isinstance(items, list) else ([items] if items else [])

            res_d = requests.get(url_dep, params=params, timeout=10)
            if res_d.status_code == 200:
                data = res_d.json()
                items = data.get('response', {}).get('body', {}).get('items', [])
                departures = items if isinstance(items, list) else ([items] if items else [])
        except:
            pass

    return render_template('index.html', arrivals=arrivals, departures=departures)

# Vercel 환경에서 로컬 테스트용
if __name__ == "__main__":
    app.run(debug=True)
