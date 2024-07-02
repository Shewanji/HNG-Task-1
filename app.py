from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name')
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # Get location and weather
    weather_api_key = 'd2680916d9ed46a8b11211922240107'
    geolocation_api_key = 'd8e0ab874e20453a8ce4a790216e9d36'

    get_location = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey={geolocation_api_key}")
    location = get_location.json()
    city = location.get('city')

    get_weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}')
    weather = get_weather.json()
    temp = weather['current']['temp_c']

    # Response in JSON
    response = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f'Hello, {visitor_name}! The temperature is {temp} degrees Celsius in {city}.'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
