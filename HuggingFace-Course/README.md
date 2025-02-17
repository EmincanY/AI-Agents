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

# HuggingFace Course Project

This project is an implementation of various Natural Language Processing (NLP) tasks and models using HuggingFace's Transformers library. It features a Gradio-based user interface for easy interaction with different NLP models and functionalities.

## Features

- Text Generation
- Sentiment Analysis
- Named Entity Recognition
- Question Answering
- Text Summarization
- Translation
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
```

4. Run the application:
```bash
python app.py
```

## Project Structure

- `app.py`: Main application file
- `Gradio_UI.py`: Gradio interface implementation
- `tools/`: Directory containing model implementations and utilities
- `prompts.yaml`: Configuration file for various model prompts
- `agent.json`: Agent configuration and settings

## Usage

The application provides a web interface where you can:
- Select different NLP tasks
- Choose from various pre-trained models
- Input your text and get instant results
- Customize model parameters
- View and compare results

## Author

This project was created by Emincan Yilmaz for learning purposes. It serves as a practical implementation of HuggingFace's Transformers library and demonstrates various NLP capabilities.
