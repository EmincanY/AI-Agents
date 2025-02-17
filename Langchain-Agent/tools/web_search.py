from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS
import html
import re

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up")
    max_results: int = Field(default=5, description="Maximum number of results to return")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web using DuckDuckGo to find information about any topic"
    args_schema: Type[BaseModel] = WebSearchInput

    def _clean_text(self, text: str) -> str:
        """Clean and format text by removing extra whitespace and unescaping HTML entities."""
        # Unescape HTML entities
        text = html.unescape(text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _run(self, query: str, max_results: int = 5) -> str:
        """Search the web using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            
            if not results:
                return f"No results found for: {query}\nTry rephrasing your query or using different keywords."
            
            # Format the results with markdown and better organization
            formatted_results = [
                f"## Web Search Results for: '{query}'\n"
                f"Found {len(results)} {'result' if len(results) == 1 else 'results'}:\n"
            ]
            
            for idx, result in enumerate(results, 1):
                # Clean and format the text
                title = self._clean_text(result['title'])
                body = self._clean_text(result['body'])
                href = result['href']
                
                # Add formatted result
                formatted_results.append(
                    f"\n### {idx}. {title}\n"
                    f"{body}\n"
                    f"🔗 [Read more]({href})\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Error performing web search: {str(e)}\n\nSuggestions:\n- Try using different search terms\n- Make your query more specific\n- Check your internet connection\n- Try again in a few moments"

    async def _arun(self, query: str, max_results: int = 5) -> str:
        """Asynchronously search the web using DuckDuckGo."""
        return self._run(query, max_results) 