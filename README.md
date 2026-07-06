# 🚀 NovaForge AI
NovaForge AI is an Autonomous Innovation Lab where multiple AI agents collaborate, debate, critique, and refine ideas into complete innovation proposals.

Unlike a normal chatbot, ForgeMind demonstrates visible multi-agent collaboration.

## 🚀 Overview

NovaForge AI is a multi-agent innovation platform that guides users from idea generation through technical analysis, economic evaluation, criticism, and proposal generation. The backend exposes FastAPI services while specialized agents coordinate the workflow. The frontend provides an interactive dashboard for creating and reviewing proposals.

### Platform capabilities

- Multi-agent orchestration
- Proposal generation
- Patent brainstorming
- Cloud cost estimation
- Security risk evaluation
- Markdown export

---
## 🌐 Live Demo

🚀 **Experience the platform live:**

- AI innovation platform using a React frontend, FastAPI backend, SQLite persistence, SQLAlchemy ORM, Pydantic validation, and MCP tooling.
  

---

## ✨ Key Features

### 🤖 Multi-Agent Workflow

Coordinator → Inventor → Engineer → Economist → Critic → Pitch Generator

### 🔌 Engine / API Architecture

- FastAPI REST endpoints
- MCP tool integration
- SQLAlchemy persistence
- Pydantic validation

### 🛡️ Security

- Prompt sanitization
- Input validation
- Typed request models
- Backend isolation

---

## 🏗️ Architecture

```text
Browser
   │
React UI
   │
FastAPI
   │
Coordinator Agent
   ├── Inventor
   ├── Engineer
   ├── Economist
   ├── Critic
   └── Pitch Generator
          │
      MCP Tools
          │
      SQLite Database
```

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
|Frontend|React|
|Backend|FastAPI|
|ORM|SQLAlchemy|
|Validation|Pydantic|
|Database|SQLite|
|Protocol|REST + MCP|

## 📂 Project Structure
## 📂 Project Structure

```bash
NovaForge/
├── backend/                  # FastAPI application layer containing agent engines
│   ├── app/
│   │   ├── agents/           # Multi-agent workflow definitions and configurations
│   │   │   ├── base.py       # Core abstract agent blueprint class
│   │   │   ├── coordinator.py# State manager orchestrating step-by-step execution
│   │   │   ├── critic.py     # Evaluation agent checking logic flaws and security
│   │   │   ├── economist.py  # Financial analyst estimating implementation costs
│   │   │   ├── engineer.py   # Developer agent structuring technical solutions
│   │   │   ├── inventor.py   # Creative agent shaping raw innovative ideas
│   │   │   └── pitch_gen.py  # Synthesizer building final presentation scripts
│   │   ├── mcp/              # Model Context Protocol client configurations
│   │   ├── database.py       # SQLite connection setup using SQLAlchemy ORM
│   │   └── main.py           # Backend server entry point mapping REST API endpoints
│   ├── mcp_server.py         # Local Model Context Protocol server exposing tools
│   ├── requirements.txt      # Main Python dependency list for backend libraries
│   ├── novaforge.db          # SQLite relational database storage file
│   ├── novaforge.db-shm      # Database temporary shared memory pointer
│   └── novaforge.db-wal      # Database Write-Ahead Logging file for write safety
├── frontend/                 # Client-side modern reactive user interface
│   ├── src/                  # React dashboard pages, components, and styling assets
│   ├── dist/                 # Production-ready optimized compiled build files
│   ├── tailwind.config.js    # UI layout styling specifications
│   └── vite.config.js        # Build tool module bundler configurations
├── cli.py                    # Terminal tool script to trigger agent runs locally
├── proposal_output.md        # Export file where final multi-agent proposals are saved
├── start.bat                 # Windows batch execution script to boot up the platform
└── test_backend.py           # Automated unit testing suite validating backend APIs


## ⚙️ Installation & Setup

### 📋 Prerequisites
Before running the application, please ensure you have the following installed on your system:
* **Python 3.10+**
* **Node.js (v18+) & npm**

---

### 🚀 1-Click Execution Method (Recommended for Examiners)

1. **Clone the repository** to your local machine:
```bash
git clone [https://github.com/windlower4596-cyber/NovaForge.git](https://github.com/windlower4596-cyber/NovaForge.git)
cd NovaForge
Double-click the startup script located in the root directory:

Bash
start.bat
This will automatically open the required terminals, start your Python background agents, launch the frontend server, and completely prepare the environment framework.

Access the application dashboard:
Open your web browser and click the link below to open the interface:

👉 http://localhost:5173

## 🔮 Future Improvements

- [ ] Authentication
- [ ] Docker Compose
- [ ] CI/CD
- [ ] Streaming responses
- [ ] Kubernetes deployment

**Author:** AYUSH SINGH

**License:** MIT

*Transforming ideas into production-ready innovation through collaborative AI agents.*

