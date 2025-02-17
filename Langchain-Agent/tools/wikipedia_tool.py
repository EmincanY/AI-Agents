from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import wikipediaapi

class WikipediaInput(BaseModel):
    query: str = Field(description="The topic to search for on Wikipedia")
    language: str = Field(default="en", description="The language of the Wikipedia article")

class WikipediaTool(BaseTool):
    name: str = "get_wikipedia_summary"
    description: str = "Get a summary of a topic from Wikipedia"
    args_schema: Type[BaseModel] = WikipediaInput

    def _run(self, query: str, language: str = "en") -> str:
        """Get Wikipedia summary for a topic."""
        try:
            wiki = wikipediaapi.Wikipedia(
                language=language,
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                user_agent="LangchainAgent/1.0"
            )
            
            # Search for the page
            page = wiki.page(query)
            
            if not page.exists():
                return f"No Wikipedia article found for: {query}"
            
            # Get the summary
            summary = page.summary[0:1500]  # Limit to 1500 characters
            if len(page.summary) > 1500:
                summary += "... (truncated)"
            
            return f"Wikipedia summary for '{query}':\n\n{summary}\n\nFull article: {page.fullurl}"
        except Exception as e:
            return f"Error fetching Wikipedia summary: {str(e)}"

    async def _arun(self, query: str, language: str = "en") -> str:
        """Async implementation of Wikipedia summary"""
        return self._run(query, language) 