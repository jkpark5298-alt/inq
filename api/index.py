from flask import Flask, render_template
import requests
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    # 환경변수에서 키를 가져오고 앞뒤 공백 제거
    api_key = os.environ.get('FLIGHT_API_KEY', '').strip()
    arrivals = []
    departures = []

    if api_key:
        try:
            # 인증키 언쿼트 처리
            service_key = requests.utils.unquote(api_key)
            # 공공데이터포털 화물기 API 주소
            url_a = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getArrivalsCargo"
            url_d = "http://apis.data.go.kr/B551177/StatusOfCargoFlights/getDeparturesCargo"
            
            params = {
                'serviceKey': service_key,
                'numOfRows': '30',
                'pageNo': '1'
            }

            def fetch_and_parse(url):
                response = requests.get(url, params=params, timeout=10)
                items_list = []
                if response.status_code == 200:
                    # XML 파싱 시작
                    root = ET.fromstring(response.content)
                    # 모든 <item> 태그를 찾아서 데이터를 담음
                    for item in root.findall('.//item'):
                        data = {}
                        for child in item:
                            data[child.tag] = child.text if child.text else ""
                        items_list.append(data)
                return items_list

            arrivals = fetch_and_parse(url_a)
            departures = fetch_and_parse(url_d)
            
        except Exception as e:
            print(f"시스템 오류 발생: {e}")

    return render_template('index.html', arrivals=arrivals, departures=departures)
