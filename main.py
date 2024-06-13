from flask import Flask, render_template, request
import requests
import json

app = Flask('app')


@app.route('/')
def index():
  
    return render_template('index.html')


@app.route('/bmi', methods=['GET'])
def bmi_form():
    return render_template('bmi.html')

@app.route('/bmi', methods=['POST'])
def bmi():
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    bmi = round(weight / ((height/100)**2), 2)
    return render_template('bmi.html', bmi=bmi)

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'Sudbury' # Default city

    api_key = 'd601670ce5387ce898d15db5258d3646'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    if data['cod'] != 200:
        return render_template('weather.html', error_message='City not found.')

    weather_description = data['weather'][0]['description']
    temperature = round(data['main']['temp'] - 273.15, 2) # Convert from Kelvin to Celsius

    return render_template('weather.html', city=city, weather_description=weather_description, temperature=temperature)

  
app.run(host='0.0.0.0', port=8080)