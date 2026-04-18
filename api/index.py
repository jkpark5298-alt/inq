from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Vercel 환경 변수에서 키를 가져오되, 없으면 빈 문자열 처리
    API_KEY = os.environ.get('FLIGHT_API_KEY', '')
    
    arrival_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
    departure_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
    
    params = {
        'serviceKey': API_KEY,
        'type': 'json',
        'airline': '', # 테스트를 위해 비워둠
        'numOfRows': '50'
    }

    arrivals = []
    departures = []

    # 데이터 가져오기 (실패해도 서버는 안 죽게 처리)
    try:
        if API_KEY:
            res_arr = requests.get(arrival_url, params=params, timeout=10)
            if res_arr.status_code == 200:
                arrivals = res_arr.json().get('response', {}).get('body', {}).get('items', [])
                if isinstance(arrivals, dict): arrivals = [arrivals]
            
            res_dep = requests.get(departure_url, params=params, timeout=10)
            if res_dep.status_code == 200:
                departures = res_dep.json().get('response', {}).get('body', {}).get('items', [])
                if isinstance(departures, dict): departures = [departures]
    except Exception:
        pass # 에러가 나면 그냥 빈 리스트로 보냄

    return render_template('index.html', arrivals=arrivals or [], departures=departures or [])
