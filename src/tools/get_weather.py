import requests
from datetime import datetime, timezone,timedelta


def get_weather(latitude=48.833195, longitude=12.961127, days_ahead=0):
    """
    Fetches the weather forecast for a specified location and date using the Bright Sky API.

    Args:
        latitude (float, optional): Latitude of the location. Defaults to Deggendorf.
        longitude (float, optional): Longitude of the location. Defaults to Deggendorf.
        days_ahead (int, optional): Number of days ahead from today for which to fetch the forecast. 
                                    Use 0 for today, 1 for tomorrow, etc. Defaults to 0.

    Returns:
        str: A formatted string with the next available weather forecast for the specified date,
             including timestamp, temperature, condition, cloud cover, and wind speed.
             If no future data is available for the selected day, a fallback message is returned.
    """

    date = (datetime.utcnow() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
    # Build request URL
    url = f"https://api.brightsky.dev/weather?lat={latitude}&lon={longitude}&date={date}"

    # Request weather data
    response = requests.get(url)
    data = response.json()

    # Get current UTC time
    now = datetime.now(timezone.utc)

    # Filter only future weather entries
    future_entries = [
        entry for entry in data.get('weather', [])
        if datetime.fromisoformat(entry['timestamp']) > now
    ]

    # Find the entry closest to now (but still in the future)
    if future_entries:
        next_weather = min(
            future_entries,
            key=lambda x: datetime.fromisoformat(x['timestamp']) - now
        )

        toReturn = ""
        toReturn += f"Next Forecast at: {next_weather['timestamp']}\n"
        toReturn += f"Temperature: {next_weather.get('temperature', 'N/A')} °C\n"
        toReturn += f"Condition: {next_weather.get('condition', 'N/A')}\n"
        toReturn += f"Cloud Cover: {next_weather.get('cloud_cover', 'N/A')}%\n"
        toReturn += f"Wind Speed: {next_weather.get('wind_speed', 'N/A')} m/s\n"
        return toReturn

    else:
        print("No future weather data available for today.")
        return "No future weather data available for today."


if __name__ == "__main__":
    # Example usage
    latitude = 48.833195  
    longitude = 12.961127  
    days_ahead = 1 
    

    weather_info = get_weather(latitude, longitude, days_ahead)
    print(weather_info)