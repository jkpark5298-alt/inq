<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>에어인천 모니터링</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen p-4">
    <div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden p-6">
        <h1 class="text-xl font-bold text-center mb-6">✈️ 에어인천 실시간 현황</h1>
        
        <input type="text" id="searchInput" placeholder="편명 검색 (예: KJ601)" 
               class="w-full p-3 border border-gray-300 rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500">

        <div class="space-y-4">
            <h2 class="font-semibold text-lg border-b pb-2">📦 운항 정보</h2>
            <div id="flightList">
                {% if arrivals or departures %}
                    {% for flight in arrivals + departures %}
                    <div class="flight-card p-4 border rounded-lg mb-3 bg-blue-50">
                        <div class="flex justify-between items-center">
                            <span class="font-bold text-blue-700">{{ flight.get('flightId', 'N/A') }}</span>
                            <span class="text-sm text-gray-500">{{ flight.get('scheduleDateTime', '')[:16] }}</span>
                        </div>
                        <div class="text-sm mt-2">
                            <p>출발지: {{ flight.get('startingAirport', '정보없음') }}</p>
                            <p>현황: <span class="text-orange-600 font-medium">{{ flight.get('remark', '운항중') }}</span></p>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="text-center text-gray-500 py-10">현재 조회된 정보가 없습니다.</p>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const term = e.target.value.toUpperCase();
            document.querySelectorAll('.flight-card').forEach(card => {
                card.style.display = card.innerText.includes(term) ? 'block' : 'none';
            });
        });
    </script>
</body>
</html>
