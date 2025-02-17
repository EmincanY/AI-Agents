from smolagents import tool
import os
import requests

@tool
def get_weather(city: str) -> str:
    """Get current weather information for a specified city
    Args:
        city: Name of the city to get weather for
    """
    # Using OpenWeatherMap API
    API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    if not API_KEY:
        return "Error: OpenWeatherMap API key not found in environment variables"
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # For Celsius
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            return f"Weather in {city}: Temperature: {temp}°C, Humidity: {humidity}%, Conditions: {description}"
        else:
            return f"Error getting weather: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}" 