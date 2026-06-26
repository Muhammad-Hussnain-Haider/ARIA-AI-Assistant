# \# 🤖 ARIA — AI Reminder \& Intelligent Assistant

# \### Kaggle 5-Day AI Agents Capstone Project · Concierge Agents Track

# 

# ARIA is a voice-enabled personal AI assistant that helps you manage your daily life — tasks, medicines, budget, and goals — powered by \*\*OpenRouter (Gemini)\*\*, \*\*MCP Server\*\*, and \*\*Supabase\*\*.

# 

# \---

# 

# \## ✨ Features

# 

# | Feature | Description |

# |---------|-------------|

# | 📋 \*\*Task Manager\*\* | Add, view, complete, delete daily tasks with priority levels |

# | 💊 \*\*Medicine Reminders\*\* | Track medicines, set reminders, mark as taken |

# | 💰 \*\*Budget Tracker\*\* | Monitor expenses, set limits, view spending summary |

# | 🎯 \*\*Goals Tracker\*\* | Set goals and track progress |

# | 🎤 \*\*Voice Input\*\* | Speak to ARIA — supports English, Urdu, Roman Urdu |

# | 🔊 \*\*Voice Output\*\* | ARIA speaks back using Text-to-Speech |

# | 🌐 \*\*Multi-language\*\* | Understands and responds in any language |

# | 🔒 \*\*Secure Auth\*\* | Login/Signup system with password hashing |

# | 🗄️ \*\*Cloud Database\*\* | Supabase PostgreSQL for persistent storage |

# 

# \---

# 

# \## 🏗️ Architecture

# 

# ```

# ┌─────────────────────────────────────────────────┐

# │                   ARIA System                   │

# ├─────────────────┬───────────────────────────────┤

# │   Frontend      │         Backend               │

# │   index.html    │         main.py (FastAPI)     │

# │   login.html    │         agent.py (Agent Loop) │

# │   - Chat UI     │         tools.py (14 Tools)   │

# │   - Voice UI    │         mcp\_server.py (MCP)   │

# │   - Dashboard   │         auth.py (Security)    │

# └─────────────────┴───────────────────────────────┘

# &#x20;        │                     │

# &#x20;        ▼                     ▼

# &#x20;  Web Browser          OpenRouter API

# &#x20;  Speech API           (Gemini Model)

# &#x20;                             │

# &#x20;                   ┌─────────┴─────────┐

# &#x20;                   │   Tool Modules    │

# &#x20;                   │ Tasks │ Medicine  │

# &#x20;                   │ Budget│ Goals     │

# &#x20;                   │ Auth  │ Summary   │

# &#x20;                   └───────────────────┘

# &#x20;                             │

# &#x20;                             ▼

# &#x20;                      Supabase DB

# &#x20;                   (PostgreSQL Cloud)

# ```

# 

# \### Key Concepts Demonstrated ✅

# \- ✅ \*\*Agentic Loop\*\* — `agent.py` with automatic tool calling (max 5 iterations)

# \- ✅ \*\*MCP Server\*\* — `mcp\_server.py` exposes 6 ARIA tools via Model Context Protocol

# \- ✅ \*\*Agent Skills/Tools\*\* — 14 tools across Tasks, Medicine, Budget, Goals modules

# \- ✅ \*\*Security\*\* — Login/Signup, password hashing (PBKDF2), session auth, `.env` secrets

# \- ✅ \*\*Cloud Database\*\* — Supabase PostgreSQL for all persistent data

# 

# \---

# 

# \## 🚀 Setup Instructions

# 

# \### Prerequisites

# \- Python 3.10+

# \- OpenRouter API Key (free at openrouter.ai)

# \- Supabase account (free at supabase.com)

# 

# \### Step 1: Clone \& Install

# 

# ```bash

# git clone https://github.com/Muhammad-Hussnain-Haider/ARIA-AI-Assistant

# cd ARIA-AI-Assistant

# pip install -r requirements.txt

# ```

# 

# \### Step 2: Configure Environment

# 

# Create `.env` file:

# ```

# OPENROUTER\_API\_KEY=your\_openrouter\_key\_here

# SUPABASE\_URL=your\_supabase\_url\_here

# SUPABASE\_KEY=your\_supabase\_key\_here

# APP\_HOST=0.0.0.0

# APP\_PORT=8000

# ```

# 

# \### Step 3: Setup Supabase Tables

# 

# Run in Supabase SQL Editor:

# ```sql

# CREATE TABLE users (

# &#x20; id bigserial PRIMARY KEY,

# &#x20; name text NOT NULL,

# &#x20; email text UNIQUE NOT NULL,

# &#x20; password\_hash text NOT NULL,

# &#x20; password\_salt text NOT NULL,

# &#x20; created\_at timestamptz DEFAULT now()

# );

# 

# CREATE TABLE tasks (

# &#x20; id bigserial PRIMARY KEY,

# &#x20; title text, time text,

# &#x20; priority text,

# &#x20; completed boolean DEFAULT false,

# &#x20; created\_at timestamptz DEFAULT now()

# );

# 

# CREATE TABLE medicines (

# &#x20; id bigserial PRIMARY KEY,

# &#x20; name text, time text,

# &#x20; dosage text, notes text,

# &#x20; taken boolean DEFAULT false,

# &#x20; created\_at timestamptz DEFAULT now()

# );

# 

# CREATE TABLE expenses (

# &#x20; id bigserial PRIMARY KEY,

# &#x20; amount numeric,

# &#x20; description text,

# &#x20; created\_at timestamptz DEFAULT now()

# );

# 

# CREATE TABLE goals (

# &#x20; id bigserial PRIMARY KEY,

# &#x20; title text, description text,

# &#x20; progress integer DEFAULT 0,

# &#x20; created\_at timestamptz DEFAULT now()

# );

# 

# CREATE TABLE settings (

# &#x20; id bigserial PRIMARY KEY,

# &#x20; key text UNIQUE,

# &#x20; value text

# );

# ```

# 

# \### Step 4: Run ARIA

# 

# ```bash

# python main.py

# ```

# 

# Open `http://localhost:8000/login` in your browser!

# 

# \---

# 

# \## 💬 Example Commands

# 

# ```

# "What are my tasks today?"

# "Add a task: Call doctor at 3 PM, high priority"

# "What medicines do I need to take?"

# "Show my budget"

# "I spent 500 rupees on food"

# "Add goal: Learn Python"

# "Give me my daily summary"

# 

# \# Urdu / Roman Urdu supported!

# "Mera schedule kya hai aaj?"

# "Budget kitna bacha hai?"

# "Dawai yaad dilao"

# ```

# 

# \---

# 

# \## 📁 Project Structure

# 

# ```

# ARIA/

# ├── main.py           # FastAPI backend server

# ├── agent.py          # Agentic loop with tool calling

# ├── tools.py          # 14 tool functions (tasks, medicine, budget, goals)

# ├── mcp\_server.py     # MCP server exposing ARIA tools

# ├── auth.py           # Authentication (login/signup/password hashing)

# ├── index.html        # Main dashboard UI

# ├── login.html        # Login/Signup page

# ├── requirements.txt  # Python dependencies

# └── README.md         # This file

# ```

# 

# \---

# 

# \## 🔒 Security Features

# 

# \- ✅ API keys in `.env` (never hardcoded)

# \- ✅ `.env` in `.gitignore`

# \- ✅ Password hashing with PBKDF2 + salt

# \- ✅ Session-based authentication

# \- ✅ CORS middleware configured

# \- ✅ Input validation via Pydantic

# 

# \---

# 

# \## 📊 Tech Stack

# 

# | Layer | Technology |

# |-------|------------|

# | AI Model | Google Gemini (via OpenRouter) |

# | Agent | Custom Agentic Loop |

# | MCP | Model Context Protocol Server |

# | Backend | Python + FastAPI |

# | Frontend | HTML + CSS + Vanilla JS |

# | Voice | Web Speech API + gTTS |

# | Database | Supabase (PostgreSQL) |

# | Auth | PBKDF2 Password Hashing |

# 

# \---

# 

# \## 👤 Author

# 

# \*\*Muhammad Hussnain Haider\*\*  

# 5-Day AI Agents: Intensive Vibe Coding Course With Google · June 2026

# 

# \---

# 

# \## 📄 License

# 

# MIT License — free to use and modify!

