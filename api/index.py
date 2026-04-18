from flask import Flask, render_template
import requests
import os

# Vercel이 가장 먼저 찾는 실행 스위치입니다.
app = Flask(__name__)

@app.route('/')
def index():
    # 1. 환경변수에서 키를 가져옵니다. (없을 경우를 대비해 빈 문자열 처리)
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    
    arrivals = []
    departures = []

    # 2. 키가 있을 때만 API 호출을 시도합니다.
    if api_key:
        try:
            # 공공데이터포털 URL
            arrival_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
            departure_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
            
            # 인증키 인코딩 문제 방지를 위해 unquote 사용
            decoded_key = requests.utils.unquote(api_key)
            
            params = {
                'serviceKey': decoded_key,
                'type': 'json',
                'numOfRows': '50'
            }

            # 도착 정보 가져오기 (실패해도 서버가 죽지 않게 try-except로 감싸기)
            try:
                res_arr = requests.get(arrival_url, params=params, timeout=5)
                if res_arr.status_code == 200:
                    data = res_arr.json()
                    items = data.get('response', {}).get('body', {}).get('items', [])
                    arrivals = items if isinstance(items, list) else ([items] if items else [])
            except:
                arrivals = []

            # 출발 정보 가져오기
            try:
                res_dep = requests.get(departure_url, params=params, timeout=5)
                if res_dep.status_code == 200:
                    data = res_dep.json()
                    items = data.get('response', {}).get('body', {}).get('items', [])
                    departures = items if isinstance(items, list) else ([items] if items else [])
            except:
                departures = []

        except Exception as e:
            # 어떤 에러가 나도 로그만 남기고 서버는 살려둡니다.
            print(f"Runtime Error: {e}")

    # 3. 데이터가 있든 없든 무조건 화면을 띄웁니다. (500 에러 방지)
    return render_template('index.html', arrivals=arrivals, departures=departures)
