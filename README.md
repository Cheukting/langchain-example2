# Python Release Newsletter Generator (LangChain + Anthropic)

Generate a polished release marketing newsletter for the latest Python version using LangChain, LangGraph, and Anthropic Claude.

The app fetches the official “What’s New in Python” page, then drafts an engaging newsletter with:
- Subject line
- Short intro paragraph
- 4–8 bullet points highlighting key features and user benefits
- Small code snippets when helpful
- “How to upgrade” section
- Links to official docs/changelog

## Requirements
- Python 3.10+
- An Anthropic API key (`ANTHROPIC_API_KEY`)

## Installation

You can install dependencies with either `uv` or `pip`.

Using uv (recommended):
```bash
uv sync
```

Using pip:
```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

Set your Anthropic API key via environment variable or a `.env` file in the project root.

Create a `.env` file like:
```
ANTHROPIC_API_KEY=your_api_key_here
# Optional overrides
ANTHROPIC_MODEL=claude-3-7-sonnet-latest
ANTHROPIC_TEMPERATURE=0.3
```

Environment variables:
- `ANTHROPIC_API_KEY` (required): Your Anthropic API key.
- `ANTHROPIC_MODEL` (optional, default `claude-3-7-sonnet-latest`): Anthropic model to use.
- `ANTHROPIC_TEMPERATURE` (optional, default `0.3`): Sampling temperature.

## Usage

Run the CLI to generate the newsletter. If `--out` is provided, the result is saved as a Markdown file; otherwise it is printed to stdout.

```bash
python main.py --out README_NEWSLETTER.md
```

Examples:
- Print to terminal:
  ```bash
  python main.py
  ```
- Save to a file:
  ```bash
  python main.py --out ./newsletter.md
  ```

## How it works

- `app/tools.py`: Defines a tool that fetches and parses the official “What’s New in Python” page.
- `app/agent.py`: Creates a LangGraph agent powered by Anthropic, guided by a purpose-built system prompt to produce the newsletter.
- `main.py`: CLI entry point that loads environment variables, runs the agent, and prints or saves the output.

Key libraries:
- `langchain` / `langchain-community`
- `langgraph` (prebuilt agent helper)
- `langchain-anthropic` (Anthropic chat model)
- `beautifulsoup4` (HTML parsing)
- `python-dotenv` (env var loading)

## Troubleshooting

- Missing API key: If you see `ERROR: ANTHROPIC_API_KEY is not set`, add it to your shell or `.env`.
- Model access: Ensure the configured Anthropic model is available to your account.
- Network errors: The tool fetches web content; make sure you have internet access.
- Version mismatch: This project pins `langgraph>=0.2.79`. If you encounter issues with the prebuilt agent helper, upgrade LangGraph:
  ```bash
  pip install -U langgraph
  # or
  uv pip install -U langgraph
  ```

## Development

- Linting: Ruff is included as an optional dev dependency.
  ```bash
  ruff check .
  ```

## License

MTI

## Disclaimer

This example project is generated with [Junie](https://www.jetbrains.com/junie/) and then examined by a human. It is not intended for production use.
