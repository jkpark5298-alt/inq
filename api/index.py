from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 1. 환경변수 확인 (Vercel에서 설정한 이름과 똑같아야 합니다)
    api_key = os.environ.get('FLIGHT_API_KEY', '')
    
    arrivals = []
    departures = []

    # 2. 인증키가 있을 때만 실행
    if api_key:
        arrival_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
        departure_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
        
        params = {
            'serviceKey': api_key,
            'type': 'json',
            'airline': '',  # 테스트를 위해 전체 항공사 조회
            'numOfRows': '50'
        }

        try:
            # 도착 정보
            res_arr = requests.get(arrival_url, params=params, timeout=10)
            if res_arr.status_code == 200:
                data = res_arr.json()
                items = data.get('response', {}).get('body', {}).get('items', [])
                arrivals = items if isinstance(items, list) else ([items] if items else [])

            # 출발 정보
            res_dep = requests.get(departure_url, params=params, timeout=10)
            if res_dep.status_code == 200:
                data = res_dep.json()
                items = data.get('response', {}).get('body', {}).get('items', [])
                departures = items if isinstance(items, list) else ([items] if items else [])
        except Exception:
            pass # 에러가 나도 화면은 띄우기 위해 무시

    # 3. 데이터가 없어도 index.html을 정상적으로 렌더링
    return render_template('index.html', arrivals=arrivals, departures=departures)
