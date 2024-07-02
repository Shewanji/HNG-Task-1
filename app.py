from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    # get location and weather using WeatherApi
    ip_api_key = 'd2680916d9ed46a8b11211922240107'
    get_location = requests.get(f'http://api.weatherapi.com/v1/ip.json?key={ip_api_key}&q={client_ip}')

    location = get_location.json()
    city = location.get('city', 'Current')

    get_weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key={ip_api_key}&q={city}')

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