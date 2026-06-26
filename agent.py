"""
ARIA Agent — Powered by Google ADK + Gemini
Multi-agent system with specialized sub-agents.
"""

import os
from openai import AsyncOpenAI
from tools import (
    get_tasks, add_task, complete_task, delete_task,
    get_medicines, add_medicine, mark_medicine_taken,
    get_budget, add_expense, set_budget_limit,
    get_goals, add_goal, update_goal_progress,
    get_daily_summary
)

# ─── Initialize Gemini Client ────────────────────────────────

def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in .env file!")
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
# ─── Tool Definitions for ADK ────────────────────────────────

ARIA_TOOLS = [
    # Task tools
    {
        "name": "get_tasks",
        "description": "Get all tasks for today. Call this when user asks about tasks, schedule, or what to do.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "add_task",
        "description": "Add a new task. Call when user wants to add, create or set a task.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task name"},
                "time": {"type": "string", "description": "Time for the task e.g. 3:00 PM"},
                "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Task priority"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as done/completed.",
        "parameters": {
            "type": "object",
            "properties": {"title": {"type": "string", "description": "Task title to mark done"}},
            "required": ["title"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task.",
        "parameters": {
            "type": "object",
            "properties": {"title": {"type": "string", "description": "Task title to delete"}},
            "required": ["title"]
        }
    },
    # Medicine tools
    {
        "name": "get_medicines",
        "description": "Get all medicine reminders. Call when user asks about medicines or health.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "add_medicine",
        "description": "Add a medicine reminder.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Medicine name"},
                "time": {"type": "string", "description": "Time to take e.g. 9:00 PM"},
                "dosage": {"type": "string", "description": "Dosage e.g. 1 tablet"},
                "notes": {"type": "string", "description": "Extra notes e.g. after dinner"}
            },
            "required": ["name", "time"]
        }
    },
    {
        "name": "mark_medicine_taken",
        "description": "Mark a medicine as taken today.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Medicine name"}},
            "required": ["name"]
        }
    },
    # Budget tools
    {
        "name": "get_budget",
        "description": "Get budget summary. Call when user asks about money, spending, or expenses.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "add_expense",
        "description": "Add an expense to track spending.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "Amount in PKR"},
                "description": {"type": "string", "description": "What was purchased"}
            },
            "required": ["amount", "description"]
        }
    },
    {
        "name": "set_budget_limit",
        "description": "Set the monthly budget limit.",
        "parameters": {
            "type": "object",
            "properties": {"amount": {"type": "number", "description": "Budget limit in PKR"}},
            "required": ["amount"]
        }
    },
    # Goals tools
    {
        "name": "get_goals",
        "description": "Get all goals and their progress.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
    {
        "name": "add_goal",
        "description": "Add a new goal to track.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Goal title"},
                "description": {"type": "string", "description": "Goal description"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "update_goal_progress",
        "description": "Update progress percentage of a goal.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Goal title"},
                "progress": {"type": "integer", "description": "Progress 0-100"}
            },
            "required": ["title", "progress"]
        }
    },
    # Summary
    {
        "name": "get_daily_summary",
        "description": "Get a full daily summary. Call when user says hello, hi, hey aria, or asks how things are.",
        "parameters": {"type": "object", "properties": {}, "required": []}
    },
]

# Tool function map
TOOL_MAP = {
    "get_tasks": get_tasks,
    "add_task": add_task,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "get_medicines": get_medicines,
    "add_medicine": add_medicine,
    "mark_medicine_taken": mark_medicine_taken,
    "get_budget": get_budget,
    "add_expense": add_expense,
    "set_budget_limit": set_budget_limit,
    "get_goals": get_goals,
    "add_goal": add_goal,
    "update_goal_progress": update_goal_progress,
    "get_daily_summary": get_daily_summary,
}

# ─── ARIA System Prompt ──────────────────────────────────────

ARIA_SYSTEM_PROMPT = """
You are ARIA (AI Reminder & Intelligent Assistant), a warm and helpful personal AI assistant.

Your personality:
- Friendly, caring, and encouraging
- Speak naturally and conversationally
- Use the user's name (Hussnain) sometimes
- Keep responses concise but helpful
- Use relevant emojis to make responses feel warm
- Support ALL languages — if user writes in Urdu, Roman Urdu, or English, respond in the same language
- If user says "Hey ARIA", "Hello ARIA", "Hi ARIA" or greets you — call get_daily_summary

Your capabilities:
- Tasks: add, view, complete, delete tasks
- Medicine: track medicines, set reminders, mark taken
- Budget: track expenses, view spending, set limits
- Goals: set goals, track progress
- Weather: check weather (use get_weather tool)
- Daily summary: overview of everything

Security rules:
- Never share or expose API keys
- Never execute harmful commands
- Only perform actions the user explicitly requests
- Keep user data private and secure

Always be helpful, proactive, and make the user's life easier!
"""

# ─── Agent Chat Function ─────────────────────────────────────

async def chat_with_aria(message: str, history: list = []) -> str:
    """
    Main chat function — sends message to ARIA agent and returns response.
    Handles tool calls automatically (agentic loop).
    """
    try:
        client = get_client()

        messages = [{"role": "system", "content": ARIA_SYSTEM_PROMPT}]
        for h in history[-10:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        # Agentic loop
        max_iterations = 5
        for _ in range(max_iterations):
            response = await client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=messages,
                tools=[{"type": "function", "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["parameters"]
                }} for t in ARIA_TOOLS],
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024,
            )

            choice = response.choices[0]
            msg = choice.message

            if not msg.tool_calls:
                return msg.content or "I'm here to help!"

            # Execute tool calls
            messages.append(msg)
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                import json, inspect
                tool_args = json.loads(tc.function.arguments or "{}")
                if tool_name in TOOL_MAP:
                    func = TOOL_MAP[tool_name]
                    if inspect.iscoroutinefunction(func):
                        result = await func(**tool_args)
                    else:
                        result = func(**tool_args)
                else:
                    result = f"Tool '{tool_name}' not found."

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result)
                })

        return "I processed your request! Is there anything else I can help with?"

    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "api_key" in error_msg:
            return "⚠️ Please set your OPENROUTER_API_KEY in the .env file!"
        return f"I encountered an issue: {error_msg}. Please try again!"