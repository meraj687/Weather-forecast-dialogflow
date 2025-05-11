# from flask import Flask
# import requests
#
#
# app = Flask(__name__)
#
# @app.route("/" )
# def index():
#     return "Hello"
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
#

# from flask import Flask , request
#
#
# app = Flask(__name__)
#
# @app.route("/" , methods = ["POST"] )
# def index():
#     data = request.get_json()
#     print(data)
#     return "Hello"
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

#------------------------------------------#

# from flask import Flask, request, jsonify
# import requests
#
# app = Flask(__name__)
#
# @app.route('/', methods=['POST'])
# def webhook():
#     data = request.get_json()
#     print("Dialogflow Request:", data)
#
#     # Get parameters from Dialogflow
#     city = data.get("queryResult", {}).get("parameters", {}).get("geo-city")
#     date_time = data.get("queryResult", {}).get("parameters", {}).get("date-time")  # Optional
#
#     if not city:
#         return jsonify({"fulfillmentText": "I didn't get the city. Please try again."})
#
#     # Fetch weather
#     weather_info = get_weather(city)
#
#     if weather_info:
#         response_text = (
#             f"The weather in {city} is {weather_info['description']} "
#             f"with a temperature of {weather_info['temp']}°C and the wind speed is {weather_info['speed']}."
#         )
#     else:
#         response_text = "Sorry, the server is under maintenance. Try again later."
#
#     return jsonify({"fulfillmentText": response_text})
#
#
# def get_weather(city):
#     API_KEY = "35a9117dae7e5f9c21ff9e596bebfc11"
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
#
#     try:
#         response = requests.get(url)
#         data = response.json()
#
#         if data.get("cod") != 200:
#             print("API returned error:", data)
#             return None
#
#         weather = {
#             "description": data["weather"][0]["description"],
#             "temp": data["main"]["temp"]
#         }
#         return weather
#
#     except Exception as e:
#         print("Error fetching weather:", e)
#         return None
#
#
# if __name__ == "__main__":
#     app.run(debug=True)

#---------------------------------------------------#
#PErfect running without error
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Dialogflow Request:", data)

    city = data.get("queryResult", {}).get("parameters", {}).get("geo-city")

    if not city:
        return jsonify({"fulfillmentText": "I didn't get the city. Please try again."})

    weather_info = get_weather(city)

    if weather_info:
        response_text = (
            f"The weather in {city} is currently {weather_info['description']} with a temperature of "
            f"{weather_info['temp']}°C (feels like {weather_info['feels_like']}°C), "
            f"humidity is {weather_info['humidity']}%, "
            f"wind is blowing at {weather_info['wind_speed']} m/s from the {weather_info['wind_dir']}"
        )
        if weather_info.get("wind_gust") is not None:
            response_text += f", with gusts up to {weather_info['wind_gust']} m/s."

        response_text += "."
    else:
        response_text = "Sorry, I couldn't fetch the weather right now. Please try again later."

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
            "wind_gust": wind.get("gust")  # optional
        }
        return weather

    except Exception as e:
        print("Weather API error:", e)
        return None


def degrees_to_compass(deg):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = round(deg / 45) % 8
    return directions[idx]


if __name__ == "__main__":
    app.run(debug=True)


#------------------------------#
#Now checking for date-time also

# from flask import Flask, request, jsonify
# import requests
# from datetime import datetime, timezone, timedelta
#
# app = Flask(__name__)
#
# @app.route('/', methods=['POST'])
# def webhook():
#     data = request.get_json()
#     print("Dialogflow Request:", data)
#
#     city = data.get("queryResult", {}).get("parameters", {}).get("geo-city")
#     date_time_str = data.get("queryResult", {}).get("parameters", {}).get("date-time")
#
#     if not city or not date_time_str:
#         return jsonify({"fulfillmentText": "I need both a city and a date to provide a forecast."})
#
#     forecast_info = get_forecast(city, date_time_str)
#
#     if forecast_info:
#         response_text = (
#             f"The weather in {city} on {forecast_info['datetime']} is expected to be "
#             f"{forecast_info['description']} with a temperature of {forecast_info['temp']}°C "
#             f"and wind speed of {forecast_info['wind_speed']} m/s."
#         )
#     else:
#         response_text = f"Sorry, I couldn't find a forecast for {city} on that date."
#
#     return jsonify({"fulfillmentText": response_text})
#
#
# def get_forecast(city, date_time_str):
#     API_KEY = "35a9117dae7e5f9c21ff9e596bebfc11"
#     url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
#
#     try:
#         response = requests.get(url)
#         data = response.json()
#
#         if data.get("cod") != "200":
#             print("API error:", data)
#             return None
#
#         # Convert Dialogflow datetime string to datetime object
#         target_time = datetime.fromisoformat(date_time_str.rstrip("Z"))
#
#         closest = None
#         min_diff = timedelta.max
#
#         for entry in data["list"]:
#             forecast_time = datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
#             diff = abs(forecast_time - target_time)
#
#             if diff < min_diff:
#                 min_diff = diff
#                 closest = entry
#
#         if closest:
#             return {
#                 "datetime": datetime.fromtimestamp(closest["dt"]).strftime("%Y-%m-%d %H:%M"),
#                 "description": closest["weather"][0]["description"],
#                 "temp": round(closest["main"]["temp"]),
#                 "wind_speed": closest["wind"]["speed"]
#             }
#
#     except Exception as e:
#         print("Forecast API error:", e)
#         return None
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


