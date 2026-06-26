# 🤖 ARIA — AI Reminder & Intelligent Assistant
### Kaggle 5-Day AI Agents Capstone Project · Concierge Agents Track

ARIA is a personal AI assistant that helps you manage your daily life — tasks, medicines, budget, and goals — powered by **OpenRouter (Gemma)**, **MCP Server**, and **Supabase**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📋 **Task Manager** | Add, view, complete, delete daily tasks with priority levels |
| 💊 **Medicine Reminders** | Track medicines, set reminders, mark as taken |
| 💰 **Budget Tracker** | Monitor expenses, set limits, view spending summary |
| 🎯 **Goals Tracker** | Set goals and track progress |
| 🌐 **Multi-language** | English, Urdu, Roman Urdu |
| 🔒 **Secure Auth** | Login/Signup with PBKDF2 password hashing |
| 🗄️ **Cloud Database** | Supabase PostgreSQL for persistent storage |

---

## 🏗️ Key Concepts Demonstrated

- ✅ **Agentic Loop** — `agent.py` auto tool calling (max 5 iterations)
- ✅ **MCP Server** — `mcp_server.py` exposes 6 tools via Model Context Protocol
- ✅ **Agent Skills** — `tools.py` has 14 specialized tool functions
- ✅ **Security** — PBKDF2 hashing, session auth, `.env` secrets
- ✅ **Cloud Database** — Supabase PostgreSQL, 6 tables

---

## 🚀 Setup

```bash
git clone https://github.com/Muhammad-Hussnain-Haider/ARIA-AI-Assistant
cd ARIA-AI-Assistant
pip install -r requirements.txt
```

Create `.env` file:
```
OPENROUTER_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
APP_HOST=0.0.0.0
APP_PORT=8000
```

Run:
```bash
python main.py
```

Open `http://localhost:8000/login`

---

## 💬 Example Commands

```
"What are my tasks today?"
"Add a task: Call doctor at 3 PM, high priority"
"I spent 500 rupees on food"
"Show my budget"
"Give me my daily summary"
"Mera schedule kya hai aaj?"
```

---

## 📁 Project Structure

```
ARIA/
├── main.py          # FastAPI backend
├── agent.py         # Agentic loop
├── tools.py         # 14 tool functions
├── mcp_server.py    # MCP server
├── auth.py          # Authentication
├── index.html       # Dashboard UI
├── login.html       # Login/Signup page
└── requirements.txt
```

---

## 📊 Tech Stack

| Layer | Technology |
|-------|------------|
| AI Model | Google Gemma 4 31B (OpenRouter) |
| Agent | Custom Agentic Loop |
| MCP | Model Context Protocol |
| Backend | Python + FastAPI |
| Frontend | HTML + CSS + Vanilla JS |
| Database | Supabase PostgreSQL |
| Auth | PBKDF2 Password Hashing |

---

**Author:** Muhammad Hussnain Haider — 5-Day AI Agents Course With Google · June 2026

**License:** MIT
