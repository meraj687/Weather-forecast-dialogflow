# Weather Chatbot (Dialogflow + Flask)

## Overview

This project is a weather chatbot that provides real-time weather and a 3-day forecast for any city. It uses Dialogflow for natural language understanding, a Flask server as the webhook, and the OpenWeatherMap API for weather data. Ngrok is used for local development to expose the Flask server to Dialogflow via HTTPS. For production, deployment can be done easily using [Render.com](https://render.com/).

---

## Features

- Get current weather for any city
- Get a 3-day weather forecast
- Conversational, user-friendly responses
- Handles errors and missing input gracefully

---

## Architecture

**Components:**
- **Dialogflow:** Handles user queries, intent recognition, and entity extraction.
- **Flask Webhook:** Receives requests from Dialogflow, fetches weather data, and returns formatted responses.
- **OpenWeatherMap API:** Provides weather and forecast data.
- **ngrok:** Exposes the local Flask server to the internet via HTTPS for Dialogflow fulfillment during development.
- **Render.com:** Cloud platform for deploying the Flask app in production.
- **Telegram Bot:** Users can also interact with the weather chatbot via Telegram using [@Weather_forcast_7054_bot](https://t.me/Weather_forcast_7054_bot).

**Flow:**
1. User sends a weather query to Dialogflow or the Telegram bot.
2. Dialogflow extracts the city and sends a POST request to the Flask webhook (ngrok HTTPS URL for local, Render.com URL for production).
3. Flask fetches weather data from OpenWeatherMap and formats the response.
4. Flask returns the response to Dialogflow, which delivers it to the user (or via Telegram).

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd Weather_forecast_py
```

### 2. Install Dependencies

```sh
pip install flask requests
```

### 3. Get OpenWeatherMap API Key

- Sign up at [OpenWeatherMap](https://openweathermap.org/api) and get your API key.
- Replace the `API_KEY` value in `app.py` with your key.

### 4. Run the Flask Server Locally

```sh
python app.py
```

The server will start on `http://localhost:5000`.

### 5. Expose Flask Server with ngrok (for local testing)

Download and install [ngrok](https://ngrok.com/), then run:

```sh
ngrok http 5000
```

Copy the HTTPS URL provided by ngrok (e.g., `https://xxxxxx.ngrok.io`).

### 6. Dialogflow Fulfillment Setup

- In Dialogflow, go to **Fulfillment** and enable the webhook.
- Set the webhook URL to your ngrok HTTPS URL (for local) or Render.com URL (for production).
- Save and deploy.

### 7. Dialogflow Intent Configuration

- Create an intent for weather queries.
- Add a parameter for the city (e.g., `geo-city`).
- Enable webhook fulfillment for the intent.

---

## Deployment on Render.com

Render.com is a cloud platform that makes it easy to deploy web services like Flask apps.

### Steps to Deploy:

1. **Push your code to GitHub.**
2. **Create a free account at [Render.com](https://render.com/).**
3. **Create a new Web Service:**
   - Click "New +" → "Web Service".
   - Connect your GitHub repo.
   - Set the build and start commands:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`
   - Choose a region and instance type (free tier is available).
4. **Set Environment Variables:**
   - Add your `API_KEY` as an environment variable if you want to keep it secret.
5. **Deploy:**
   - Render will build and deploy your app.
   - You will get a public HTTPS URL (e.g., `https://your-app.onrender.com/`).
6. **Update Dialogflow:**
   - Set your webhook URL in Dialogflow Fulfillment to the Render.com URL.

---

## Telegram Bot

You can also use the weather chatbot on Telegram:  
👉 [@Weather_forcast_7054_bot](https://t.me/Weather_forcast_7054_bot)

---

## Example Usage

**User:** "What's the weather in Berlin?"

**Bot:**  
🌤️ Current weather in Berlin:  
Clear sky, 22°C (feels like 21°C), humidity 60%, wind 3 m/s from NW.  
📅 3-day forecast:  
Wednesday, Jun 04: Clear sky, 23°C, wind 2.5 m/s  
Thursday, Jun 05: Few clouds, 21°C, wind 3.1 m/s  
Friday, Jun 06: Light rain, 19°C, wind 4.0 m/s  

---

## Notes

- For local development, always keep your Flask server and ngrok running when testing with Dialogflow.
- For production, Render.com provides a stable HTTPS endpoint.
- Keep your API key secure and do not commit it to public repositories.
- For production, consider using environment variables for sensitive data.

---

## License

This project is for educational purposes.