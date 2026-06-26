# 🤖 ARIA — AI Reminder & Intelligent Assistant
### Kaggle 5-Day AI Agents Capstone Project · Concierge Agents Track

ARIA is a voice-enabled personal AI assistant that helps you manage your daily life — tasks, medicines, budget, weather, and goals — powered by **Google ADK**, **Gemini 2.0 Flash**, and **MCP servers**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📋 **Task Manager** | Add, view, complete, delete daily tasks with priority levels |
| 💊 **Medicine Reminders** | Track medicines, set reminders, mark as taken |
| 💰 **Budget Tracker** | Monitor expenses, set limits, view spending summary |
| 🌤️ **Weather** | Real-time weather for any city |
| 🎯 **Goals Tracker** | Set goals and track progress |
| 🎤 **Voice Input** | Speak to ARIA — supports English, Urdu, Roman Urdu |
| 🔊 **Voice Output** | ARIA speaks back using Text-to-Speech |
| 👂 **Wake Word** | Say "Hey ARIA" to activate hands-free |
| 🌐 **Multi-language** | Understands and responds in any language |
| 🔒 **Secure** | No API keys in code, local data storage |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   ARIA System                   │
├─────────────────┬───────────────────────────────┤
│   Frontend      │         Backend               │
│   index.html    │         main.py (FastAPI)     │
│   - Chat UI     │         agent.py (ADK)        │
│   - Voice UI    │         tools.py (Modules)    │
│   - Dashboard   │         mcp_server.py (MCP)   │
└─────────────────┴───────────────────────────────┘
         │                     │
         ▼                     ▼
   Web Browser          Google Gemini 2.0
   Speech API           (via Google ADK)
                              │
                    ┌─────────┴─────────┐
                    │   Tool Modules    │
                    │ Tasks │ Medicine  │
                    │ Budget│ Weather   │
                    │ Goals │ Summary   │
                    └───────────────────┘
```

### Key Concepts Used (Course Requirements ✅)
- ✅ **Multi-agent system (ADK)** — ARIA agent with specialized tool calling
- ✅ **MCP Server** — `mcp_server.py` exposes tools via Model Context Protocol
- ✅ **Antigravity** — Used for development and deployment
- ✅ **Security features** — API key in `.env`, no hardcoded secrets, input validation
- ✅ **Deployability** — FastAPI server, ready for Cloud Run deployment
- ✅ **Agent skills (CLI)** — Antigravity CLI used for project scaffolding

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Google AI Studio API Key (free at aistudio.google.com)
- Antigravity 2.0 + IDE + CLI installed

### Step 1: Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/aria-assistant
cd aria-assistant
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```
GOOGLE_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_openweathermap_key_here  # optional
```

### Step 3: Run ARIA

```bash
python main.py
```

Then open `http://localhost:8000` in your browser!

### Step 4: Run MCP Server (optional)

```bash
python mcp_server.py
```

---

## 💬 How to Use

### Chat Mode
1. Click the purple **💬** button on the right side
2. Type your message and press Enter
3. ARIA will respond with relevant information

### Voice Mode
1. Click the 🎤 mic button in the header
2. Tap the circle mic button OR say **"Hey ARIA"**
3. Speak your request — ARIA listens and responds with voice!

### Example Commands
```
"What are my tasks today?"
"Add a task: Call doctor at 3 PM, high priority"
"Mark morning walk as done"
"What medicines do I need to take?"
"Add medicine: Vitamin C at 8 AM, 1 tablet"
"Show my budget"
"I spent 500 rupees on food"
"What's the weather in Karachi?"
"Add goal: Learn Python"
"Update goal Learn Python to 75%"
"Give me my daily summary"
```

### Urdu / Roman Urdu Support
```
"Mera schedule kya hai aaj?"
"Dawai yaad dilao"
"Budget kitna bacha hai?"
```

---

## 📁 Project Structure

```
ARIA/
├── main.py           # FastAPI backend server
├── agent.py          # Google ADK agent with Gemini
├── tools.py          # All tool modules (tasks, medicine, etc.)
├── mcp_server.py     # MCP server for Antigravity integration
├── index.html        # Complete frontend UI
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variables template
├── .env              # Your actual keys (DO NOT commit this!)
└── README.md         # This file
```

---

## 🔒 Security Features

- ✅ API keys stored in `.env` file (never in code)
- ✅ `.env` added to `.gitignore`
- ✅ CORS middleware configured
- ✅ Input validation via Pydantic models
- ✅ No sensitive data in responses
- ✅ Local JSON storage (user data stays on device)
- ⚠️ **Never share your API key with anyone!**

---

## 🌐 Deploy to Cloud Run

```bash
# Build and deploy
gcloud run deploy aria-assistant \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key_here
```

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | Google Gemini 2.0 Flash |
| Agent Framework | Google ADK (Agent Development Kit) |
| MCP | Model Context Protocol Server |
| Backend | Python + FastAPI |
| Frontend | HTML + CSS + Vanilla JS |
| Voice | Web Speech API + gTTS |
| Storage | Local JSON file |
| Dev Tools | Antigravity 2.0, IDE, CLI |

---

## 👤 Author

**Muhammad Hussnain Haider**  
Kaggle: kaggle.com/profile  
5-Day AI Agents: Intensive Vibe Coding Course With Google · June 2026

---

## 📄 License

MIT License — free to use and modify!
