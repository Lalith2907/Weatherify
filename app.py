from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'your_api_key'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if city:
        response = requests.get(f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric")
        
        if response.status_code == 200:
            weather_data = response.json()
            temp_c = weather_data['main']['temp']
            temp_f = (temp_c * 9/5) + 32

            return render_template('weather.html', current=weather_data, temp_c=temp_c, temp_f=temp_f)
        else:
            error_message = weather_data.get('message', 'Unknown error. Please try again later.')
            return render_template('layout.html', error=error_message)
    
    return render_template('layout.html', error='Please enter a city.')

if __name__ == '__main__':
    app.run(debug=True)
