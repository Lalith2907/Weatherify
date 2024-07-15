from flask import Flask, render_template, request, session, redirect, url_for
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = 'your_key'

API_KEY = 'your_api_key'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if city:
        weather_response = requests.get(f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric")
        
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            
            forecast_response = requests.get(f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric")
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                
                daily_forecasts = {}
                for entry in forecast_data['list']:
                    timestamp = entry['dt']
                    date = datetime.utcfromtimestamp(timestamp).date()
                    
                    if date not in daily_forecasts:
                        daily_forecasts[date] = {
                            'date': date,
                            'temp': entry['main']['temp'],
                            'description': entry['weather'][0]['description']
                        }
                
                forecast_list = list(daily_forecasts.values())
                
                temp_c = weather_data['main']['temp']
                temp_f = (temp_c * 9/5) + 32

                return render_template('weather.html', current=weather_data, temp_c=temp_c, temp_f=temp_f, forecast_list=forecast_list)
            else:
                error_message = 'Failed to fetch forecast data. Please try again.'
        else:
            error_message = 'Failed to fetch weather data. Please try again.'
        
        return render_template('layout.html', error=error_message)
    
    return render_template('layout.html', error='Please enter a city.')

@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    if 'theme' in session:
        session['theme'] = 'dark' if session['theme'] == 'light' else 'light'
    else:
        session['theme'] = 'light'
    
    return redirect(request.referrer or '/')

if __name__ == '__main__':
    app.run(debug=True)