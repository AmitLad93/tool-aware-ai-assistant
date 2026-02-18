# AI Assistant with Tool Support

## What is this project?

This project is a **simple AI assistant** that runs in the terminal (command line). You type questions in plain English, and it responds like a chat.

The key feature is that when an answer needs to be **exact** (for example, a calculation), the assistant calls a **normal Python function** instead of guessing.

---

## Why this project exists

Language models are great at text, but they are **not reliable calculators** and should not be trusted to apply fixed business rules without controls.

This project demonstrates a practical pattern used in real AI systems:

> Let the AI decide **when** a tool is needed, but let traditional code decide **how** the work is done.

This keeps outcomes:
- **Accurate** (math is done in Python)
- **Explainable** (tool calls are visible)
- **Easy to test** (tools are deterministic)

---

## What happens when you use it?

1. You type a message.
2. The AI reads it and decides whether it can answer directly.
3. If needed, it calls an approved Python **tool** (e.g., arithmetic or greetings).
4. The terminal prints a clear message when a tool is called.
5. The assistant returns the final answer.

---

## Example interaction

```text
You: Divide 10 by 4 and round to 2 decimals

--- TOOL CALLED: perform_arithmetic ---
Inputs -> first_value=10, second_value=4, operation=divide
-------------------------------------

Assistant: Result: 2.5
```

---

## What skills this demonstrates

### AI / Data Science thinking
- Practical use of **LLMs** for intent understanding and response generation
- Awareness of LLM limitations (e.g., arithmetic accuracy)
- Controlled AI behaviour: AI can *choose* tools, but not change tool logic

### Software engineering
- Clean, readable **Python**
- Clear separation between conversational AI and deterministic logic
- Input validation and safe error handling

### Responsible AI design
- Deterministic tools for anything that must be correct
- Transparent behaviour (you can *see* tool usage)
- Easy path to adding auditing, logging, and governance controls later

---

## One-sentence summary

**An AI assistant that chats naturally but routes calculations and fixed logic through trusted Python tools, making behaviour accurate and transparent.**
