from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from app.agent import run_newsletter


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Generate a Python release marketing newsletter with LangChain + Anthropic."
    )
    parser.add_argument(
        "--out", type=Path, help="Optional path to save the newsletter markdown."
    )
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print(
            "ERROR: ANTHROPIC_API_KEY is not set. Set it in your environment or a .env file."
        )
        return 1

    print("Fetching latest Python features and generating newsletter...\n")
    output = run_newsletter()
    if args.out:
        args.out.write_text(output, encoding="utf-8")
        print(f"Saved newsletter to {args.out}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
