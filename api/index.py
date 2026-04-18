from flask import Flask, render_template
import requests
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    # Vercel Settings에 등록한 'Decoding' 인증키를 가져옵니다.
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        try:
            # 인증키의 특수문자를 올바르게 처리합니다.
            service_key = requests.utils.unquote(api_key)
            
            # 1. 모든 항공사 출발 정보 (최대 50건)
            dep_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
            res_d = requests.get(dep_url, params={'serviceKey': service_key, 'numOfRows': '50'}, timeout=15)
            
            if res_d.status_code == 200:
                root = ET.fromstring(res_d.text)
                for item in root.findall('.//item'):
                    departures.append({
                        'flightId': item.findtext('flightId', '-'),
                        'remark': item.findtext('remark', '준비중'),
                        'arrAirport': item.findtext('airport', '-'),
                        'estimatedDateTime': item.findtext('estimatedDateTime', '000000000000')
                    })

            # 2. 모든 항공사 도착 정보 (최대 50건)
            arr_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
            res_a = requests.get(arr_url, params={'serviceKey': service_key, 'numOfRows': '50'}, timeout=15)
            
            if res_a.status_code == 200:
                root = ET.fromstring(res_a.text)
                for item in root.findall('.//item'):
                    arrivals.append({
                        'flightId': item.findtext('flightId', '-'),
                        'remark': item.findtext('remark', '운항중'),
                        'depAirport': item.findtext('airport', '-'),
                        'estimatedDateTime': item.findtext('estimatedDateTime', '000000000000')
                    })
        except Exception as e:
            # 오류 발생 시 로그에서 확인 가능하도록 출력
            print(f"시스템 오류 발생: {e}")

    return render_template('index.html', arrivals=arrivals, departures=departures)
