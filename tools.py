"""
ARIA Tools — All modules: Tasks, Medicine, Budget, Weather, Goals
Each function is a tool that the agent can call.
Fully connected to Supabase PostgreSQL database.
"""
import os
import httpx
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ── Supabase client ────────────────────────────────────────────────────────────
def get_db():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env!")
    return create_client(url, key)

# ── Load all data (for /data endpoint) ────────────────────────────────────────
def load_data() -> dict:
    try:
        db = get_db()
        tasks     = db.table("tasks").select("*").order("created_at", desc=False).execute().data or []
        medicines = db.table("medicines").select("*").order("created_at", desc=False).execute().data or []
        expenses  = db.table("expenses").select("*").order("created_at", desc=False).execute().data or []
        goals     = db.table("goals").select("*").order("created_at", desc=False).execute().data or []
        settings  = db.table("settings").select("*").execute().data or []

        budget_limit = 60000
        for s in settings:
            if s.get("key") == "budget_limit":
                budget_limit = float(s.get("value", 60000))

        return {
            "tasks": tasks,
            "medicines": medicines,
            "expenses": expenses,
            "goals": goals,
            "budget_limit": budget_limit,
        }
    except Exception as e:
        return {"tasks": [], "medicines": [], "expenses": [], "goals": [], "budget_limit": 60000, "error": str(e)}

# ════════════════════════════════════════════════════════════
# TASKS
# ════════════════════════════════════════════════════════════
def add_task(title: str, time: str = "", priority: str = "med") -> str:
    try:
        db = get_db()
        db.table("tasks").insert({
            "title": title,
            "time": time,
            "priority": priority,
            "done": False
        }).execute()
        return f"✅ Task add ho gaya: '{title}'"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_task(title: str) -> str:
    try:
        db = get_db()
        rows = db.table("tasks").select("*").ilike("title", f"%{title}%").execute().data
        if not rows:
            return f"Task '{title}' nahi mila!"
        db.table("tasks").delete().eq("id", rows[0]["id"]).execute()
        return f"🗑️ Task delete: '{rows[0]['title']}'"
    except Exception as e:
        return f"Error: {str(e)}"

def complete_task(title: str) -> str:
    try:
        db = get_db()
        rows = db.table("tasks").select("*").ilike("title", f"%{title}%").execute().data
        if not rows:
            return f"Task '{title}' nahi mila!"
        db.table("tasks").update({"done": True}).eq("id", rows[0]["id"]).execute()
        return f"✅ Task complete: '{rows[0]['title']}'"
    except Exception as e:
        return f"Error: {str(e)}"

def get_tasks() -> str:
    try:
        db = get_db()
        rows = db.table("tasks").select("*").order("created_at").execute().data or []
        if not rows:
            return "📋 Koi task nahi hai abhi."
        pending = [t for t in rows if not t.get("done")]
        done    = [t for t in rows if t.get("done")]
        result  = f"📋 Tasks ({len(rows)} total):\n"
        for t in pending:
            result += f"  ⬜ [{t.get('priority','med').upper()}] {t['title']}"
            if t.get("time"):
                result += f" at {t['time']}"
            result += "\n"
        for t in done:
            result += f"  ✅ {t['title']}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# ════════════════════════════════════════════════════════════
# MEDICINES
# ════════════════════════════════════════════════════════════
def add_medicine(name: str, time: str = "", dosage: str = "1 dose") -> str:
    try:
        db = get_db()
        db.table("medicines").insert({
            "name": name,
            "time": time,
            "dosage": dosage,
            "taken": False
        }).execute()
        return f"💊 Medicine add ho gayi: '{name}' at {time}"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_medicine(name: str) -> str:
    try:
        db = get_db()
        rows = db.table("medicines").select("*").ilike("name", f"%{name}%").execute().data
        if not rows:
            return f"Medicine '{name}' nahi mili!"
        db.table("medicines").delete().eq("id", rows[0]["id"]).execute()
        return f"🗑️ Medicine delete: '{rows[0]['name']}'"
    except Exception as e:
        return f"Error: {str(e)}"

def toggle_medicine(name: str) -> str:
    try:
        db = get_db()
        rows = db.table("medicines").select("*").ilike("name", f"%{name}%").execute().data
        if not rows:
            return f"Medicine '{name}' nahi mili!"
        new_val = not rows[0].get("taken", False)
        db.table("medicines").update({"taken": new_val}).eq("id", rows[0]["id"]).execute()
        status = "✅ Li gayi" if new_val else "⬜ Reset"
        return f"{status}: '{rows[0]['name']}'"
    except Exception as e:
        return f"Error: {str(e)}"

def get_medicines() -> str:
    try:
        db = get_db()
        rows = db.table("medicines").select("*").order("time").execute().data or []
        if not rows:
            return "💊 Koi medicine reminder nahi hai."
        result = f"💊 Medicines ({len(rows)}):\n"
        for m in rows:
            status = "✅" if m.get("taken") else "⬜"
            result += f"  {status} {m['name']} — {m.get('dosage','1 dose')}"
            if m.get("time"):
                result += f" at {m['time']}"
            result += "\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# ════════════════════════════════════════════════════════════
# BUDGET / EXPENSES
# ════════════════════════════════════════════════════════════
def add_expense(amount: float, description: str, category: str = "Other") -> str:
    try:
        db = get_db()
        db.table("expenses").insert({
            "amount": amount,
            "description": description,
            "category": category
        }).execute()
        return f"💰 Expense add: PKR {amount:,.0f} — {description}"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_expense(expense_id: int) -> str:
    try:
        db = get_db()
        db.table("expenses").delete().eq("id", expense_id).execute()
        return f"🗑️ Expense deleted (id: {expense_id})"
    except Exception as e:
        return f"Error: {str(e)}"

def get_budget() -> str:
    try:
        db = get_db()
        expenses = db.table("expenses").select("*").execute().data or []
        settings = db.table("settings").select("*").eq("key", "budget_limit").execute().data or []
        budget_limit = float(settings[0]["value"]) if settings else 60000
        total_spent  = sum(e.get("amount", 0) for e in expenses)
        remaining    = budget_limit - total_spent

        result = f"💰 Budget Summary:\n"
        result += f"  Limit:     PKR {budget_limit:,.0f}\n"
        result += f"  Spent:     PKR {total_spent:,.0f}\n"
        result += f"  Remaining: PKR {remaining:,.0f}\n\n"

        if expenses:
            result += "Recent expenses:\n"
            for e in expenses[-5:]:
                result += f"  • {e['description']} — PKR {e['amount']:,.0f} [{e.get('category','Other')}]\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# ════════════════════════════════════════════════════════════
# GOALS
# ════════════════════════════════════════════════════════════
def add_goal(title: str, progress: int = 0) -> str:
    try:
        db = get_db()
        db.table("goals").insert({
            "title": title,
            "progress": max(0, min(100, progress))
        }).execute()
        return f"🎯 Goal add: '{title}' ({progress}%)"
    except Exception as e:
        return f"Error: {str(e)}"

def update_goal(title: str, progress: int) -> str:
    try:
        db = get_db()
        rows = db.table("goals").select("*").ilike("title", f"%{title}%").execute().data
        if not rows:
            return f"Goal '{title}' nahi mila!"
        db.table("goals").update({"progress": max(0, min(100, progress))}).eq("id", rows[0]["id"]).execute()
        return f"🎯 Goal updated: '{rows[0]['title']}' → {progress}%"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_goal(title: str) -> str:
    try:
        db = get_db()
        rows = db.table("goals").select("*").ilike("title", f"%{title}%").execute().data
        if not rows:
            return f"Goal '{title}' nahi mila!"
        db.table("goals").delete().eq("id", rows[0]["id"]).execute()
        return f"🗑️ Goal delete: '{rows[0]['title']}'"
    except Exception as e:
        return f"Error: {str(e)}"

def get_goals() -> str:
    try:
        db = get_db()
        rows = db.table("goals").select("*").order("created_at").execute().data or []
        if not rows:
            return "🎯 Koi goal set nahi hai."
        result = f"🎯 Goals ({len(rows)}):\n"
        for g in rows:
            bar = "█" * (g.get("progress", 0) // 10) + "░" * (10 - g.get("progress", 0) // 10)
            result += f"  {g['title']}: [{bar}] {g.get('progress', 0)}%\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# ════════════════════════════════════════════════════════════
# WEATHER
# ════════════════════════════════════════════════════════════
def get_weather(city: str = "Rawalpindi") -> str:
    try:
        api_key = os.getenv("WEATHER_API_KEY", "")
        if not api_key:
            return f"🌤️ Weather API key nahi hai. Set WEATHER_API_KEY in .env"
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        with httpx.Client(timeout=10) as client:
            resp = client.get(url)
            data = resp.json()
        loc  = data["location"]
        cur  = data["current"]
        cond = cur["condition"]["text"]
        return (
            f"🌤️ Weather in {loc['name']}, {loc['country']}:\n"
            f"  🌡️ {cur['temp_c']}°C (feels like {cur['feelslike_c']}°C)\n"
            f"  ☁️ {cond}\n"
            f"  💧 Humidity: {cur['humidity']}%\n"
            f"  💨 Wind: {cur['wind_kph']} km/h"
        )
    except Exception as e:
        return f"Weather fetch nahi hua: {str(e)}"