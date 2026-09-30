"""Tool-calling smoke test using a DeepSeek model via the OpenAI-compatible API.

Configuration is loaded from the gitignored .env file at the project root.
Key, base URL and model id are pulled from DEEPSEEK_API_KEY / DEEPSEEK_BASE_URL / DEEPSEEK_MODEL.

Important: never hard-code the API key in source. If the .env file is missing or
DEEPSEEK_API_KEY is the REPLACE_WITH_NEW_KEY placeholder, the script exits early
with a clear message instead of sending a broken request.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from smolagents import OpenAIServerModel, ToolCallingAgent, tool

# Resolve the project root (one level above examples/) so the .env file lookup
# is independent of the working directory from which the script is invoked.
_PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
load_dotenv(_PROJECT_ROOT / ".env")


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First addend (integer).
        b: Second addend (integer).

    Returns:
        The sum of ``a`` and ``b``.
    """
    return a + b


def _require_env(name: str) -> str:
    """Return the env var or exit with a clear message if it is missing or unset."""

    value = os.environ.get(name, "")
    if not value or "REPLACE_WITH" in value:
        sys.stderr.write(
            f"error: {name} is missing or still a placeholder. "
            f"Edit .env at the project root and provide a real value.\n"
        )
        sys.exit(2)
    return value


def main() -> None:
    print("=== tool metadata ===")
    print("name:", add_numbers.name)
    print("description:", add_numbers.description)
    print("inputs:", add_numbers.inputs)
    print("output_type:", add_numbers.output_type)

    api_key = _require_env("DEEPSEEK_API_KEY")
    api_base = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model_id = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro")

    # OpenAIServerModel walks the OpenAI-compatible protocol, which is what DeepSeek exposes.
    model = OpenAIServerModel(
        model_id=model_id,
        api_base=api_base,
        api_key=api_key,
        max_tokens=1000,
        # smolagents 1.26 默认 tool_choice="required"，DeepSeek 在 thinking 模式下不兼容，
        # 覆盖为 "auto" 让模型自行判断是否调用工具。
        tool_choice="auto",
    )
    # ToolCallingAgent.__init__ takes **kwargs and forwards them to
    # MultiStepAgent.__init__, which accepts description and max_steps.
    agent = ToolCallingAgent(
        tools=[add_numbers],
        model=model,
        max_steps=5,
        description="Demo agent that can only add two integers.",
    )

    print("=== run ===")
    result = agent.run("Use the add_numbers tool to compute 2 + 4.")
    print("final answer:", result)

    print("=== replay ===")
    agent.replay(detailed=True)


if __name__ == "__main__":
    main()