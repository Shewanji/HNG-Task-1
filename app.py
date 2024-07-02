from flask import Flask, request, jsonify
import requests
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

weather_api_key = 'd2680916d9ed46a8b11211922240107'
geolocation_api_key = '7b38a3fffa68f4'

def get_client_ip():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    print(f"Client IP: {client_ip}")
    return client_ip

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'visitor')
    client_ip = get_client_ip()
    # get location and weather
    get_location = requests.get(f'https://ipinfo.io/{client_ip}?token={geolocation_api_key}')
    location = get_location.json()
    city = location.get('city')

    get_weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}')
    weather = get_weather.json()
    temp = weather['current']['temp_c']

    #response in json
    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}!, the temperature is {temp} degrees Celsius in {city}'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)