---
title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.15.0
app_file: app.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- agent-course
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# AI Agent with SmolaGents

This project implements an AI agent using the SmolaGents library, featuring various custom tools for different functionalities. The agent is equipped with a Gradio UI for easy interaction and uses a HuggingFace endpoint for inference.

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
- Interactive UI with Gradio

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

3. Set up your `.env` file with necessary API keys:
```
HUGGINGFACE_API_KEY=your_huggingface_api_key
NEWS_API_KEY=your_news_api_key
```

4. Run the application:
```bash
python app.py
```

## Project Structure

- `app.py`: Main application file with agent configuration
- `Gradio_UI.py`: Gradio interface implementation
- `tools/`: Directory containing custom tool implementations
- `prompts.yaml`: System prompts and templates for the agent
- `agent.json`: Agent configuration and settings

## Usage

The application provides a web interface where you can:
- Interact with the AI agent through natural language
- Access various tools and functionalities
- Get real-time responses for different tasks
- View conversation history
- Customize agent parameters

## Author

This project was created by Emincan Yilmaz for learning purposes. It demonstrates the implementation of AI agents using the SmolaGents library and showcases various tool integrations and capabilities.
