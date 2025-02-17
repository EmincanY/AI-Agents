# Langchain Agent with Custom Tools

This project implements an AI agent using Langchain, featuring various custom tools for different functionalities. The agent is equipped with a Gradio UI for easy interaction.

## Features

- Weather information
- Currency conversion
- News headlines
- Wikipedia summaries
- Math expressions
- Password generation
- Time zone conversion
- Web search (DuckDuckGo)
- Webpage visiting

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
NEWS_API_KEY=your_news_api_key
```

4. Run the application:
```bash
python app.py
```

## Project Structure

- `app.py`: Main application file
- `tools/`: Directory containing custom tool implementations
- `gradio_ui.py`: Gradio interface implementation
- `prompts.py`: System prompts and templates for the agent 