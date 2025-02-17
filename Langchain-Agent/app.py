from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from dotenv import load_dotenv
import bs4
import gradio as gr
import os
from langchain_core.utils.function_calling import convert_to_openai_function

from tools import (
    WeatherTool,
    CurrencyTool,
    NewsTool,
    WikipediaTool,
    MathTool,
    PasswordTool,
    TimeTool,
    WebSearchTool,
    WebpageTool,
)

# Load environment variables
load_dotenv()

# Initialize tools
tools = [
    WeatherTool(),
    CurrencyTool(),
    NewsTool(),
    WikipediaTool(),
    MathTool(),
    PasswordTool(),
    TimeTool(),
    WebSearchTool(),
    WebpageTool(),
]

# Initialize the language model
model = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo",
)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant with access to various tools.
    Your goal is to help users with their questions and tasks using the available tools.
    Always provide clear and concise responses, and use the most appropriate tool for each task.
    If you're unsure about something, ask for clarification.
    
    Available tools:
    - Weather information
    - Currency conversion
    - News headlines
    - Wikipedia summaries
    - Math expressions
    - Password generation
    - Time zone conversion
    - Web search
    - Webpage content extraction"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create the Langchain agent
functions = [convert_to_openai_function(t) for t in tools]
agent = create_openai_functions_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Initialize chat history
chat_history = []

def process_message(message, history):
    # Add the new message to chat history
    chat_history.append({"role": "user", "content": message})
    
    # Execute the agent
    response = agent_executor.invoke({
        "input": message,
        "chat_history": chat_history
    })
    
    # Add the agent's response to chat history
    chat_history.append({"role": "assistant", "content": response["output"]})
    
    return response["output"]

# Create Gradio interface
iface = gr.ChatInterface(
    process_message,
    title="AI Assistant with Tools",
    description="""Ask me anything! I have various tools at my disposal:
    - Get weather information for any location
    - Convert between currencies
    - Search for news headlines
    - Get Wikipedia summaries
    - Solve math expressions
    - Generate secure passwords
    - Get current time in different timezones
    - Search the web
    - Extract content from webpages""",
    theme="soft",
)

if __name__ == "__main__":
    iface.launch(share=True) 