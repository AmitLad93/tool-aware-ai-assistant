"""
Simple AI Assistant with Tool Support (Beginner-Friendly)

This script runs a small AI assistant in the terminal.

Key idea:
- The AI decides *when* a tool is needed
- Python code performs the exact logic
- The terminal clearly shows when a tool is called
"""

from __future__ import annotations

import os
from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent


# ------------------------------------------------------------
# Environment setup
# ------------------------------------------------------------

def load_env_or_fail() -> None:
    """
    Load environment variables from a .env file.

    We check this upfront so configuration problems
    are obvious immediately.
    """
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Add it to your .env file."
        )


# ------------------------------------------------------------
# Tools: trusted Python logic
# ------------------------------------------------------------

@tool
def perform_arithmetic(
    first_value: float,
    second_value: float,
    operation: Literal["add", "subtract", "multiply", "divide"] = "add",
    round_to: Optional[int] = None,
) -> str:
    """
    Perform a basic arithmetic calculation.

    We keep this as plain Python so the result
    is always correct and easy to understand.
    """
    print("\n--- TOOL CALLED: perform_arithmetic ---")
    print(
        f"Inputs -> first_value={first_value}, "
        f"second_value={second_value}, "
        f"operation={operation}"
    )
    print("-------------------------------------")

    if operation == "divide" and second_value == 0:
        raise ValueError("Cannot divide by zero.")

    if operation == "add":
        result = first_value + second_value
    elif operation == "subtract":
        result = first_value - second_value
    elif operation == "multiply":
        result = first_value * second_value
    else:  # divide
        result = first_value / second_value

    # Optional rounding to keep output tidy
    if round_to is not None:
        if not isinstance(round_to, int) or round_to < 0 or round_to > 10:
            raise ValueError("round_to must be an integer between 0 and 10.")
        result = round(result, round_to)

    return f"Result: {result}"


@tool
def generate_greeting(
    name: str,
    style: Literal["friendly", "professional"] = "friendly",
) -> str:
    """
    Generate a simple greeting.

    This shows how wording and tone can be
    controlled in code rather than guessed by the AI.
    """
    print("\n--- TOOL CALLED: generate_greeting ---")
    print(f"Inputs -> name='{name}', style='{style}'")
    print("------------------------------------")

    cleaned_name = (name or "").strip()
    if not cleaned_name:
        raise ValueError("Name cannot be empty.")

    # Keep name formatting conservative
    cleaned_name = cleaned_name[0].upper() + cleaned_name[1:]

    if style == "professional":
        return f"Good day, {cleaned_name}."

    return f"Hello {cleaned_name}! Hope you're doing well."


# ------------------------------------------------------------
# Build the agent
# ------------------------------------------------------------

def build_agent():
    """
    Create the AI agent and explicitly grant access
    only to the approved tools.
    """
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,  # predictable behaviour
    )

    tools = [
        perform_arithmetic,
        generate_greeting,
    ]

    return create_react_agent(model, tools)


# ------------------------------------------------------------
# Command-line interface
# ------------------------------------------------------------

def run_cli(agent) -> None:
    """
    Simple interactive loop for talking to the assistant.
    """
    print("Welcome! Type 'quit' to exit.\n")

    while True:
        user_text = input("You: ").strip()

        if not user_text:
            continue

        if user_text.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            return

        try:
            result = agent.invoke(
                {"messages": [HumanMessage(content=user_text)]}
            )

            # The final assistant reply is always the last message
            final_message = result["messages"][-1]
            print(f"\nAssistant: {final_message.content}\n")

        except Exception as exc:
            print(f"[Error] {exc}\n")


# ------------------------------------------------------------
# Application entry point
# ------------------------------------------------------------

def main() -> None:
    """
    Start the application.
    """
    load_env_or_fail()
    agent = build_agent()
    run_cli(agent)


if __name__ == "__main__":
    main()