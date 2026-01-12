# LangChain Python Release Newsletter Generator

A simple Python application that uses a LangChain agent and OpenAI's GPT-4o to automatically generate a marketing newsletter for the latest Python release by scraping the official "What's New in Python" documentation.

## Features

- **Automated Web Scraping**: Fetches the latest Python release highlights from `docs.python.org`.
- **AI-Powered Generation**: Uses a LangChain agent with a specialized system prompt to craft a professional newsletter.
- **Markdown Output**: Generates a formatted newsletter including subject lines, key features, and code snippets.
- **CLI Interface**: Easy-to-use command-line interface with options to output to console or save to a file.

## Prerequisites

- Python 3.14+ (as specified in `pyproject.toml`)
- An OpenAI API Key

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/cheuktingho/LangChainExample2.git
   cd LangChainExample2
   ```

2. Install dependencies (using `uv` is recommended):
   ```bash
   uv sync
   ```
   Or using `pip`:
   ```bash
   pip install .
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o  # Optional, defaults to gpt-4o
   ```

## Usage

Run the script to generate a newsletter and print it to the console:

```bash
uv run main.py
```

To save the newsletter to a file:

```bash
uv run main.py --out newsletter.md
```

## Project Structure

- `main.py`: The entry point of the application. Handles CLI arguments and environment loading.
- `app/`:
    - `agent.py`: Defines the LangChain agent, system prompt, and execution logic.
    - `tools.py`: Contains the custom scraping tool `fetch_python_whatsnew` used by the agent.
- `pyproject.toml`: Project configuration and dependencies.

## How it Works

1. The agent is initialized with a system prompt that defines its role as a Product Marketing Manager at the Python Software Foundation.
2. The agent uses the `fetch_python_whatsnew` tool to:
    - Scrape the index page of "What's New in Python".
    - Find the latest version's article.
    - Extract and clean the relevant highlights.
3. The agent then processes this information to draft a structured newsletter based on the requirements in the system prompt.

## License

MIT

## Disclaimer

This example project is generated with [Junie](https://www.jetbrains.com/junie/) and then examined and edited by a human. It is not intended for production use.
