from __future__ import annotations

import os

from langchain.agents import create_agent

from .tools import fetch_python_whatsnew

from dotenv import load_dotenv


SYSTEM_PROMPT = (
    "You are a senior Product Marketing Manager at the Python Software Foundation. "
    "Task: Draft a clear, engaging release marketing newsletter for end users and developers, "
    "highlighting the most compelling new features, performance improvements, and quality-of-life "
    "changes in the latest Python release.\n\n"
    "Process: Use the tool to fetch the latest 'What's New in Python' page. Read the highlights and craft "
    "a concise newsletter with: (1) an attention-grabbing subject line, (2) a short intro paragraph, "
    "(3) 4–8 bullet points of key features with user benefits, (4) short code snippets only if they add clarity, "
    "(5) a 'How to upgrade' section, and (6) links to official docs/changelog. Keep it accurate and avoid speculation."
)


def run_newsletter() -> str:
    load_dotenv()

    agent = create_agent(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        tools=[fetch_python_whatsnew],
        system_prompt=SYSTEM_PROMPT,
        # response_format=ToolStrategy(ResponseFormat),
    )

    messages = "Use the tool to fetch the latest 'What's New in Python' and then write the release marketing newsletter."
    # result = agent.invoke({"messages": messages})
    # import pdb; pdb.set_trace()
    result = agent.invoke({"messages": [{"role": "user", "content": messages}]})


    # LangGraph agents return a state dict with a `messages` list; take the last AI message
    msgs = result.get("messages", [])
    if not msgs:
        return ""
    last = msgs[-1]
    # Support both BaseMessage objects and dict-like fallbacks
    content = getattr(last, "content", None)
    if isinstance(content, str):
        return content
    # If content is a list of parts or message is dict-like
    if isinstance(content, list):
        # Join text parts if present
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                parts.append(part["text"])
        if parts:
            return "\n".join(parts)
    if isinstance(last, dict):
        return str(last.get("content", ""))
    return ""
