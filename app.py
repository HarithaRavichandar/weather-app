from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# ✅ Your API key (works after activation)
API_KEY = "6f9222a50685170dacbf5485bfda230d"

@app.route('/', methods=['GET', 'POST'])
def weather():
    city = ""
    temperature = "N/A"
    description = "Enter a city to get weather info."
    icon_url = None
    weather_main = "default"
    country = ""
    date_time = ""

    if request.method == 'POST':
        city = request.form['city'].strip()

        # ✅ Build API URL
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=en&appid={API_KEY}"

        # 🔍 Send API request
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            city = data['name']
            country = data['sys']['country']
            temperature = f"{data['main']['temp']}°C"
            description = data['weather'][0]['description'].capitalize()
            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            # 🌤️ Used for background styling
            weather_main = data['weather'][0]['main'].lower()

            # 🕒 Local time conversion
            timezone_offset = data['timezone']  # in seconds
            local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
            date_time = local_time.strftime("%A, %d %B %Y • %I:%M %p")
        else:
            # ❌ If city not found
            description = "City not found!"
            weather_main = "error"

    # 🔁 Pass values to HTML
    return render_template(
        'index.html',
        city=city,
        country=country,
        temperature=temperature,
        description=description,
        icon_url=icon_url,
        weather_main=weather_main,
        date_time=date_time
    )

if __name__ == "__main__":
    app.run(debug=True)
