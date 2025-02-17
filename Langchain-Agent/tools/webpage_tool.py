from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import re

class WebpageInput(BaseModel):
    url: str = Field(description="The URL of the webpage to visit")

class WebpageTool(BaseTool):
    name: str = "visit_webpage"
    description: str = "Visit a webpage and extract its main content"
    args_schema: Type[BaseModel] = WebpageInput

    def _run(self, url: str) -> str:
        """Visit a webpage and extract its content."""
        try:
            # Add scheme if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fetch the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long
            if len(text) > 1500:
                text = text[:1500] + "... (content truncated)"
            
            return f"Content from {url}:\n\n{text}"
        except requests.exceptions.RequestException as e:
            return f"Error accessing webpage: {str(e)}"
        except Exception as e:
            return f"Error processing webpage: {str(e)}"

    async def _arun(self, url: str) -> str:
        """Async implementation of webpage visiting"""
        return self._run(url) 