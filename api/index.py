from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 환경변수 키 확인
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        try:
            # 인증키 디코딩 (공공데이터포털 특유의 키 문제 해결)
            service_key = requests.utils.unquote(api_key)
            
            # API 호출 공통 파라미터
            params = {'serviceKey': service_key, 'type': 'json', 'numOfRows': '50'}

            # 도착 정보
            res_a = requests.get("http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo", params=params, timeout=10)
            if res_a.status_code == 200:
                arrivals = res_a.json().get('response', {}).get('body', {}).get('items', [])

            # 출발 정보
            res_d = requests.get("http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo", params=params, timeout=10)
            if res_d.status_code == 200:
                departures = res_d.json().get('response', {}).get('body', {}).get('items', [])
        except:
            pass

    # 리스트가 단일 객체일 경우를 대비한 안전 장치
    if not isinstance(arrivals, list): arrivals = [arrivals] if arrivals else []
    if not isinstance(departures, list): departures = [departures] if departures else []

    return render_template('index.html', arrivals=arrivals, departures=departures)
