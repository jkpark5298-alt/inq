from flask import Flask, render_template, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# 공공데이터포털 인증키 (Vercel 환경 변수에서 가져옴)
API_KEY = os.environ.get('FLIGHT_API_KEY')

@app.route('/')
def index():
    # 인천공항 화물기 운항 현황 API 주소
    arrival_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
    departure_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
    
    # API 요청 매개변수
    # 테스트를 위해 'airline'을 빈값으로 설정하여 모든 항공사를 불러옵니다.
    params = {
        'serviceKey': API_KEY,
        'type': 'json',
        'airline': '',  # 에어인천만 보려면 나중에 'AIAS'로 수정
        'numOfRows': '50'
    }

    arrivals = []
    departures = []

    try:
        # 도착 정보 호출
        res_arr = requests.get(arrival_url, params=params, timeout=5)
        if res_arr.status_code == 200:
            data = res_arr.json()
            arrivals = data.get('response', {}).get('body', {}).get('items', [])
            # 데이터가 단일 객체일 경우 리스트로 변환
            if isinstance(arrivals, dict):
                arrivals = [arrivals]
            elif not arrivals:
                arrivals = []

        # 출발 정보 호출
        res_dep = requests.get(departure_url, params=params, timeout=5)
        if res_dep.status_code == 200:
            data = res_dep.json()
            departures = data.get('response', {}).get('body', {}).get('items', [])
            if isinstance(departures, dict):
                departures = [departures]
            elif not departures:
                departures = []

    except Exception as e:
        print(f"Error: {e}")

    return render_template('index.html', arrivals=arrivals, departures=departures)

if __name__ == '__main__':
    app.run(debug=True)
