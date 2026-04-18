import os
from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder='../templates')

# 공공데이터포털에서 발급받은 인증키를 Vercel 환경변수(FLIGHT_API_KEY)에 등록해야 합니다.
SERVICE_KEY = os.environ.get('FLIGHT_API_KEY')

def get_flight_data(mode="Arrivals"):
    """인천공항 화물기 운항 현황 조회 (에어인천 필터링)"""
    base_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlightsDSOdp"
    endpoint = "/getArrivalsDSOdp" if mode == "Arrivals" else "/getDeparturesDSOdp"
    
    # api/index.py 내용 일부
params = {
    'serviceKey': os.environ.get('FLIGHT_API_KEY'),
    'type': 'json',
    'numOfRows': '20'
}
    
    try:
        # 인증키가 없을 경우 예외 처리
        if not SERVICE_KEY:
            return []
            
        res = requests.get(base_url + endpoint, params=params, timeout=10)
        data = res.json()
        return data.get('response', {}).get('body', {}).get('items', [])
    except Exception as e:
        print(f"Error fetching {mode}: {e}")
        return []

@app.route('/')
def index():
    arrivals = get_flight_data("Arrivals")
    departures = get_flight_data("Departures")
    return render_template('index.html', arrivals=arrivals, departures=departures)

# Vercel 배포를 위한 설정
app.debug = False
