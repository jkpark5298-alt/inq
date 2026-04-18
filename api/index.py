from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        # 인증키 뒤에 붙는 특수문자 문제를 방지하기 위해 쌩(raw) 키를 사용하거나
        # 필요한 경우 requests가 알아서 인코딩하도록 맡깁니다.
        arrival_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
        departure_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
        
        params = {
            'serviceKey': requests.utils.unquote(api_key), # 키 인코딩 문제 방지
            'type': 'json',
            'airline': '', 
            'numOfRows': '50'
        }

        try:
            # 도착 정보 조회
            res_arr = requests.get(arrival_url, params=params, timeout=10)
            if res_arr.status_code == 200:
                data = res_arr.json()
                body = data.get('response', {}).get('body', {})
                items = body.get('items', [])
                # 데이터가 없을 때(None)나 딕셔너리일 때를 모두 리스트로 변환
                if not items: arrivals = []
                elif isinstance(items, dict): arrivals = [items]
                else: arrivals = items

            # 출발 정보 조회
            res_dep = requests.get(departure_url, params=params, timeout=10)
            if res_dep.status_code == 200:
                data = res_dep.json()
                body = data.get('response', {}).get('body', {})
                items = body.get('items', [])
                if not items: departures = []
                elif isinstance(items, dict): departures = [items]
                else: departures = items
        except Exception:
            pass 

    return render_template('index.html', arrivals=arrivals, departures=departures)
