"""
ARIA Backend — FastAPI Server
Handles chat, voice, auth, and all API endpoints.
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import AsyncOpenAI

load_dotenv()

app = FastAPI(title="ARIA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent

# ── OpenRouter client ──────────────────────────────────────────────────────────
def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in .env file!")
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

# ── ARIA system prompt ─────────────────────────────────────────────────────────
ARIA_SYSTEM_PROMPT = """You are ARIA (AI-powered Responsive Intelligent Assistant), a warm and helpful personal AI assistant.

You help manage:
- Tasks and to-dos
- Medicine reminders
- Budget and expenses
- Goals and progress
- Weather information

Always respond in a friendly tone. You can respond in Urdu or English based on what the user writes.
When the user asks to add, delete, or update something, use the appropriate tool.
Always confirm actions with a friendly message.
"""

# ── Tools ──────────────────────────────────────────────────────────────────────
ARIA_TOOLS = [
    {"name":"add_task","description":"Add a new task","parameters":{"type":"object","properties":{"title":{"type":"string"},"time":{"type":"string"},"priority":{"type":"string","enum":["high","med","low"]}},"required":["title"]}},
    {"name":"delete_task","description":"Delete a task","parameters":{"type":"object","properties":{"title":{"type":"string"}},"required":["title"]}},
    {"name":"complete_task","description":"Mark task as done","parameters":{"type":"object","properties":{"title":{"type":"string"}},"required":["title"]}},
    {"name":"get_tasks","description":"Get all tasks","parameters":{"type":"object","properties":{}}},
    {"name":"add_medicine","description":"Add medicine reminder","parameters":{"type":"object","properties":{"name":{"type":"string"},"time":{"type":"string"},"dosage":{"type":"string"}},"required":["name"]}},
    {"name":"delete_medicine","description":"Delete medicine","parameters":{"type":"object","properties":{"name":{"type":"string"}},"required":["name"]}},
    {"name":"get_medicines","description":"Get all medicines","parameters":{"type":"object","properties":{}}},
    {"name":"add_expense","description":"Add an expense","parameters":{"type":"object","properties":{"amount":{"type":"number"},"description":{"type":"string"},"category":{"type":"string"}},"required":["amount","description"]}},
    {"name":"get_budget","description":"Get budget summary","parameters":{"type":"object","properties":{}}},
    {"name":"add_goal","description":"Add a goal","parameters":{"type":"object","properties":{"title":{"type":"string"},"progress":{"type":"integer"}},"required":["title"]}},
    {"name":"update_goal","description":"Update goal progress","parameters":{"type":"object","properties":{"title":{"type":"string"},"progress":{"type":"integer"}},"required":["title","progress"]}},
    {"name":"delete_goal","description":"Delete a goal","parameters":{"type":"object","properties":{"title":{"type":"string"}},"required":["title"]}},
    {"name":"get_goals","description":"Get all goals","parameters":{"type":"object","properties":{}}},
    {"name":"get_weather","description":"Get weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}},
]

from tools import (
    add_task, delete_task, complete_task, get_tasks,
    add_medicine, delete_medicine, get_medicines,
    add_expense, get_budget,
    add_goal, update_goal, delete_goal, get_goals,
    get_weather, delete_expense, toggle_medicine
)

TOOL_MAP = {
    "add_task": add_task, "delete_task": delete_task,
    "complete_task": complete_task, "get_tasks": get_tasks,
    "add_medicine": add_medicine, "delete_medicine": delete_medicine,
    "get_medicines": get_medicines, "add_expense": add_expense,
    "get_budget": get_budget, "add_goal": add_goal,
    "update_goal": update_goal, "delete_goal": delete_goal,
    "get_goals": get_goals, "get_weather": get_weather,
}

chat_histories: dict = {}

# ── Models ─────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class AuthRequest(BaseModel):
    email: str
    password: str
    name: str = ""

# ── Auth helper ────────────────────────────────────────────────────────────────
def get_current_user(request: Request) -> dict | None:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    from auth import verify_token
    return verify_token(auth[7:])

# ── Auth routes ────────────────────────────────────────────────────────────────
@app.post("/auth/signup")
async def signup_route(data: AuthRequest):
    try:
        from auth import signup
        return signup(data.name, data.email, data.password)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/auth/login")
async def login_route(data: AuthRequest):
    try:
        from auth import login
        return login(data.email, data.password)
    except ValueError as e:
        raise HTTPException(401, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/auth/me")
async def me_route(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user

# ── Chat ───────────────────────────────────────────────────────────────────────
async def chat_with_aria(message: str, history: list) -> str:
    try:
        client = get_client()
        messages = [{"role": "system", "content": ARIA_SYSTEM_PROMPT}]
        for h in history[-10:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        for _ in range(5):
            response = await client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=messages,
                tools=[{"type": "function", "function": {"name": t["name"], "description": t["description"], "parameters": t["parameters"]}} for t in ARIA_TOOLS],
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1024,
            )
            choice = response.choices[0]
            msg = choice.message
            if not msg.tool_calls:
                return msg.content or "I'm here to help!"
            messages.append(msg)
            for tc in msg.tool_calls:
                import json, inspect
                tool_args = json.loads(tc.function.arguments or "{}")
                func = TOOL_MAP.get(tc.function.name)
                if func:
                    result = await func(**tool_args) if inspect.iscoroutinefunction(func) else func(**tool_args)
                else:
                    result = f"Tool '{tc.function.name}' not found."
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})

        return "Request process ho gaya! Kuch aur chahiye?"
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg:
            return "⚠️ OPENROUTER_API_KEY set karein .env mein!"
        return f"Error: {error_msg}"

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def root():
    f = BASE_DIR / "index.html"
    return HTMLResponse(f.read_text(encoding="utf-8") if f.exists() else "<h1>ARIA</h1>")

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    f = BASE_DIR / "login.html"
    return HTMLResponse(f.read_text(encoding="utf-8") if f.exists() else "<h1>Login</h1>")

@app.post("/chat")
async def chat(req: ChatRequest):
    history = chat_histories.get(req.session_id, [])
    reply = await chat_with_aria(req.message, history)
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": reply})
    chat_histories[req.session_id] = history[-20:]
    return {"reply": reply, "session_id": req.session_id}

@app.get("/data")
async def get_data():
    from tools import load_data
    return load_data()

@app.post("/add_task")
async def add_task_direct(data: dict):
    return {"result": add_task(data.get("title",""), data.get("time",""), data.get("priority","med"))}

@app.post("/delete_task")
async def delete_task_direct(data: dict):
    return {"result": delete_task(data.get("title",""))}

@app.post("/toggle_task")
async def toggle_task_direct(data: dict):
    return {"result": complete_task(data.get("title",""))}

@app.post("/add_expense")
async def add_expense_direct(data: dict):
    return {"result": add_expense(data.get("amount",0), data.get("description",""), data.get("category","Other"))}

@app.post("/delete_expense")
async def delete_expense_direct(data: dict):
    return {"result": delete_expense(data.get("id",0))}

@app.post("/add_medicine")
async def add_medicine_direct(data: dict):
    return {"result": add_medicine(data.get("name",""), data.get("time",""), data.get("dosage","1 dose"))}

@app.post("/delete_medicine")
async def delete_medicine_direct(data: dict):
    return {"result": delete_medicine(data.get("name",""))}

@app.post("/toggle_medicine")
async def toggle_medicine_direct(data: dict):
    return {"result": toggle_medicine(data.get("name",""))}

@app.post("/add_goal")
async def add_goal_direct(data: dict):
    return {"result": add_goal(data.get("title",""), data.get("progress",0))}

@app.post("/delete_goal")
async def delete_goal_direct(data: dict):
    return {"result": delete_goal(data.get("title",""))}

@app.post("/update_goal")
async def update_goal_direct(data: dict):
    return {"result": update_goal(data.get("title",""), data.get("progress",0))}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)