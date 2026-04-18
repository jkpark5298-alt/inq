from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Vercel Settings에 등록한 인증키 가져오기
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        try:
            # 인증키 디코딩 처리
            service_key = requests.utils.unquote(api_key)
            # 공공데이터포털 API 파라미터 설정
            params = {'serviceKey': service_key, 'type': 'json', 'numOfRows': '100'}

            # 1. 화물기 도착 정보 호출
            res_a = requests.get("http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo", params=params, timeout=10)
            if res_a.status_code == 200:
                raw_arrivals = res_a.json().get('response', {}).get('body', {}).get('items', [])
                if not isinstance(raw_arrivals, list): raw_arrivals = [raw_arrivals]
                # 에어인천(KJ) 편명만 필터링
                arrivals = [item for item in raw_arrivals if str(item.get('flightId', '')).startswith('KJ')]

            # 2. 화물기 출발 정보 호출
            res_d = requests.get("http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo", params=params, timeout=10)
            if res_d.status_code == 200:
                raw_departures = res_d.json().get('response', {}).get('body', {}).get('items', [])
                if not isinstance(raw_departures, list): raw_departures = [raw_departures]
                # 에어인천(KJ) 편명만 필터링
                departures = [item for item in raw_departures if str(item.get('flightId', '')).startswith('KJ')]
        except:
            # 에러 발생 시 빈 리스트 반환
            pass

    return render_template('index.html', arrivals=arrivals, departures=departures)
