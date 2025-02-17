from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import pytz
from datetime import datetime

class TimeInput(BaseModel):
    timezone: str = Field(description="The timezone to get current time for (e.g., 'America/New_York', 'Europe/London')")

class TimeTool(BaseTool):
    name: str = "get_current_time_in_timezone"
    description: str = "Get the current time in a specific timezone"
    args_schema: Type[BaseModel] = TimeInput

    def _run(self, timezone: str) -> str:
        """Get current time in specified timezone."""
        try:
            # Validate timezone
            if timezone not in pytz.all_timezones:
                close_matches = [tz for tz in pytz.all_timezones if timezone.lower() in tz.lower()]
                if close_matches:
                    return f"Invalid timezone. Did you mean one of these?\n" + "\n".join(close_matches[:5])
                return f"Invalid timezone: {timezone}"
            
            # Get current time in specified timezone
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            
            # Format the response
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            offset = current_time.strftime("%z")
            
            return f"Current time in {timezone}:\n{formatted_time} (UTC{offset})"
        except Exception as e:
            return f"Error getting time: {str(e)}"

    async def _arun(self, timezone: str) -> str:
        """Async implementation of timezone conversion"""
        return self._run(timezone) 