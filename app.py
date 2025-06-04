from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET' , 'POST'])
def webhook():

    if request.method == 'GET':
        return "✅ Weather Webhook is running!", 200
    
    # Handle POST request from Dialogflow
    data = request.get_json()
    print("Dialogflow Request:", data)

    city = data.get("queryResult", {}).get("parameters", {}).get("geo-city")

    if not city:
        return jsonify({"fulfillmentText": "I didn't get the city. Please try again."})

    weather_info = get_weather(city)
    forecast_info = get_3_day_forecast(city)

    if not weather_info:
        return jsonify({"fulfillmentText": "Sorry, I couldn't fetch the weather right now. Please try again later."})

    # Current weather
    response_text = (
        f"🌤️ Current weather in {city}:\n"
        f"{weather_info['description'].capitalize()}, {weather_info['temp']}°C "
        f"(feels like {weather_info['feels_like']}°C), "
        f"humidity {weather_info['humidity']}%, "
        f"wind {weather_info['wind_speed']} m/s from {weather_info['wind_dir']}"
    )
    if weather_info.get("wind_gust") is not None:
        response_text += f", gusts up to {weather_info['wind_gust']} m/s"
    response_text += ".\n\n"

    # 3-day forecast
    if forecast_info:
        response_text += "📅 3-day forecast:\n"
        for day in forecast_info:
            response_text += (
                f"{day['date']}: {day['description'].capitalize()}, "
                f"{day['temp']}°C, wind {day['wind_speed']} m/s\n"
            )
    else:
        response_text += "❌ Forecast data is not available right now."

    return jsonify({"fulfillmentText": response_text})


def get_weather(city):
    API_KEY = "35a9117dae7e5f9c21ff9e596bebfc11"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            print("API error:", data)
            return None

        wind = data.get("wind", {})
        wind_dir = degrees_to_compass(wind.get("deg", 0))

        weather = {
            "description": data["weather"][0]["description"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "wind_speed": wind.get("speed"),
            "wind_dir": wind_dir,
            "wind_gust": wind.get("gust")
        }
        return weather

    except Exception as e:
        print("Weather API error:", e)
        return None


def get_3_day_forecast(city):
    API_KEY = "35a9117dae7e5f9c21ff9e596bebfc11"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            print("Forecast API error:", data)
            return None

        today = datetime.utcnow().date()
        daily_summary = {}

        for entry in data["list"]:
            dt = datetime.utcfromtimestamp(entry["dt"])
            date = dt.date()
            if today <= date < today + timedelta(days=3):
                if date not in daily_summary:
                    daily_summary[date] = {
                        "temps": [],
                        "winds": [],
                        "descriptions": []
                    }
                daily_summary[date]["temps"].append(entry["main"]["temp"])
                daily_summary[date]["winds"].append(entry["wind"]["speed"])
                daily_summary[date]["descriptions"].append(entry["weather"][0]["description"])

        forecast_list = []
        for date, values in daily_summary.items():
            forecast_list.append({
                "date": date.strftime("%A, %b %d"),
                "temp": round(sum(values["temps"]) / len(values["temps"])),
                "wind_speed": round(sum(values["winds"]) / len(values["winds"]), 1),
                "description": max(set(values["descriptions"]), key=values["descriptions"].count)
            })

        return forecast_list

    except Exception as e:
        print("Forecast API error:", e)
        return None


def degrees_to_compass(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = round(deg / 45) % 8
    return directions[idx]


if __name__ == "__main__":
    app.run(debug=True)

