from flask import Flask, render_template
import requests
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        try:
            # 인증키 디코딩 및 URL 설정
            service_key = requests.utils.unquote(api_key)
            
            # 1. 출발 정보 처리 (Departures)
            dep_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
            dep_params = {'serviceKey': service_key, 'numOfRows': '100'}
            res_d = requests.get(dep_url, params=dep_params, timeout=10)
            
            if res_d.status_code == 200:
                root = ET.fromstring(res_d.text)
                for item in root.findall('.//item'):
                    f_id = item.findtext('flightId', '')
                    if f_id.startswith('KJ'):
                        departures.append({
                            'flightId': f_id,
                            'remark': item.findtext('remark', '준비중'),
                            'arrAirport': item.findtext('airport', '-'),
                            'estimatedDateTime': item.findtext('estimatedDateTime', '000000000000')
                        })

            # 2. 도착 정보 처리 (Arrivals)
            arr_url = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
            arr_params = {'serviceKey': service_key, 'numOfRows': '100'}
            res_a = requests.get(arr_url, params=arr_params, timeout=10)
            
            if res_a.status_code == 200:
                root = ET.fromstring(res_a.text)
                for item in root.findall('.//item'):
                    f_id = item.findtext('flightId', '')
                    if f_id.startswith('KJ'):
                        arrivals.append({
                            'flightId': f_id,
                            'remark': item.findtext('remark', '운항중'),
                            'depAirport': item.findtext('airport', '-'),
                            'estimatedDateTime': item.findtext('estimatedDateTime', '000000000000')
                        })
        except Exception as e:
            print(f"Error: {e}")

    return render_template('index.html', arrivals=arrivals, departures=departures)
