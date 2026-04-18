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
            service_key = requests.utils.unquote(api_key)
            # 데이터를 명시적으로 JSON으로 요청하되, 안 될 경우를 대비합니다.
            params = {'serviceKey': service_key, 'type': 'json', 'numOfRows': '50'}
            
            # 도착 정보 호출
            res_a = requests.get("http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo", params=params, timeout=10)
            # 출발 정보 호출
            res_d = requests.get("http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo", params=params, timeout=10)

            def parse_data(response):
                # JSON 응답인 경우
                if response.status_code == 200 and 'json' in response.headers.get('Content-Type', ''):
                    return response.json().get('response', {}).get('body', {}).get('items', [])
                # XML 응답인 경우 (현재 종규님의 상황)
                elif response.status_code == 200:
                    root = ET.fromstring(response.content)
                    items = []
                    for item_node in root.findall('.//item'):
                        item_dict = {child.tag: child.text for child in item_node}
                        items.append(item_dict)
                    return items
                return []

            arrivals = parse_data(res_a)
            departures = parse_data(res_d)
            
        except Exception as e:
            print(f"Error: {e}")

    return render_template('index.html', arrivals=arrivals, departures=departures)
