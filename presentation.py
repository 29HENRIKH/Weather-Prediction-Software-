import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Constants
API_KEY = "ed15a27d48afeca1b9d406ea30cc5e06"  
# Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def fetch_weather_forecast(location, event_date):
    """
    Fetches weather forecast data for a specific location and event date.
    """
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  
        # Raise an error for bad status codes
        weather_data = response.json()

        # Extract relevant forecast data for the event date
        event_forecast = []
        for forecast in weather_data['list']:
            forecast_date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            if forecast_date == event_date:
                event_forecast.append({
                    "datetime": datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                    "temperature": forecast['main']['temp'],
                    "humidity": forecast['main']['humidity'],
                    "weather": forecast['weather'][0]['description'],
                    "wind_speed": forecast['wind']['speed']
                })
        return event_forecast
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None

def analyze_weather_forecast(forecast):
    """Analyzes the weather forecast and provides recommendations for event planning."""
    if not forecast:
        messagebox.showinfo("No Data", "No forecast data available.")
        return

    result_text = "\nWeather Forecast for Event:\n"
    for entry in forecast:
        result_text += f"Time: {entry['datetime']}\n"
        result_text += f"Temperature: {entry['temperature']}°C\n"
        result_text += f"Humidity: {entry['humidity']}%\n"
        result_text += f"Weather: {entry['weather']}\n"
        result_text += f"Wind Speed: {entry['wind_speed']} m/s\n"
        result_text += "-" * 30 + "\n"

    # Provide recommendations based on weather conditions
    for entry in forecast:
        if "rain" in entry['weather'].lower():
            result_text += "Recommendation: Advise attendees to bring umbrellas or raincoats.\n"
        if entry['temperature'] > 30:
            result_text += "Recommendation: Provide shaded areas and water stations for attendees.\n"
        if entry['wind_speed'] > 10:
            result_text += "Recommendation: Secure tents and outdoor decorations due to high winds.\n"

    messagebox.showinfo("Weather Forecast", result_text)

def on_submit():
    """Handles the submit button click event."""
    location = location_entry.get()
    event_date = date_entry.get()

    if not location or not event_date:
        messagebox.showwarning("Input Error", "Please enter both location and event date.")
        return

    forecast = fetch_weather_forecast(location, event_date)
    if forecast:
        analyze_weather_forecast(forecast)

# Create the main window
root = tk.Tk()
root.title("Weather Forecast App")

# Create and place the location label and entry
location_label = tk.Label(root, text="Event Location (e.g., 'New York, US'):")
location_label.grid(row=0, column=0, padx=10, pady=10)
location_entry = tk.Entry(root, width=30)
location_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place the date label and entry
date_label = tk.Label(root, text="Event Date (YYYY-MM-DD):")
date_label.grid(row=1, column=0, padx=10, pady=10)
date_entry = tk.Entry(root, width=30)
date_entry.grid(row=1, column=1, padx=10, pady=10)

# Create and place the submit button
submit_button = tk.Button(root, text="Get Weather Forecast", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Start the main event loop
root.mainloop()

