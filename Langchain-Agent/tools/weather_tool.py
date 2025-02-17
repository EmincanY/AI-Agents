from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import requests
import os

class WeatherInput(BaseModel):
    location: str = Field(description="The city or location to get weather information for")

class WeatherTool(BaseTool):
    name: str = "get_weather"
    description: str = "Get current weather information for a specific location"
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, location: str) -> str:
        """Use this tool to get weather information for a location."""
        try:
            # Using OpenWeatherMap API (you'll need to add API key to .env)
            api_key = os.getenv("OPENWEATHERMAP_API_KEY")
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            
            params = {
                "q": location,
                "appid": api_key,
                "units": "metric"
            }
            
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                weather_desc = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                
                return f"Weather in {location}:\n" \
                       f"- Condition: {weather_desc}\n" \
                       f"- Temperature: {temp}°C\n" \
                       f"- Humidity: {humidity}%\n" \
                       f"- Wind Speed: {wind_speed} m/s"
            else:
                return f"Error getting weather for {location}: {data.get('message', 'Unknown error')}"
                
        except Exception as e:
            return f"Error getting weather information: {str(e)}"

    async def _arun(self, location: str) -> str:
        """Async implementation of the weather tool"""
        return self._run(location) 