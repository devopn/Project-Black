import os
from flask import Flask, jsonify, request

from service.city import get_city_info
from service.weather import get_daily_weather
from models.weather import Weather

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.get('/health')
def health():
    if os.environ.get('API_KEY') is None:
        return jsonify({'status': 'error'}), 500
    return jsonify({'status': 'ok'}), 200

@app.get('/get_weather')
def get_weather():
    city = request.args.get('city')
    interval = request.args.get('interval')
    if city is None or interval is None:
        return jsonify({'error': 'Missing required parameters, city and interval'}), 400
    
    try:
        city_data = get_city_info(city)
        weather_data = get_daily_weather(city_data['key'])[:int(interval)]
        weather_pr = [
            Weather(**day).__dict__ for day in weather_data
        ]
        result = {
            'city': city,
            'weather': weather_pr
        }
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

