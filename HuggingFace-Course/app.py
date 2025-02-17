from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool
import yaml
import os
from dotenv import load_dotenv
from tools.final_answer import FinalAnswerTool
from tools.weather_tool import get_weather
from tools.currency_tool import convert_currency
from tools.news_tool import get_news_headlines
from tools.wikipedia_tool import get_wikipedia_summary
from tools.math_tool import solve_math_expression
from tools.password_tool import generate_password
from tools.time_tool import get_current_time_in_timezone
from tools.web_search import DuckDuckGoSearchTool
from tools.visit_webpage import VisitWebpageTool
from Gradio_UI import GradioUI

# Load environment variables
load_dotenv()

# Initialize the model
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud',
    custom_role_conversions=None,
)

# Load prompt templates
with open("prompts.yaml", 'r', encoding='utf-8') as stream:
    prompt_templates = yaml.safe_load(stream)

# Initialize final answer tool
final_answer = FinalAnswerTool()

# Initialize web tools
web_search_tool = DuckDuckGoSearchTool(max_results=5)
visit_webpage_tool = VisitWebpageTool()
    
# Initialize the agent with all tools
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        get_weather,
        convert_currency,
        get_news_headlines,
        get_wikipedia_summary,
        solve_math_expression,
        generate_password,
        get_current_time_in_timezone,
        web_search_tool,
        visit_webpage_tool
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

# Launch the Gradio interface
GradioUI(agent).launch()