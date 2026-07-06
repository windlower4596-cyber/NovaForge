# ✨ NovaForge AI 🚀

NovaForge AI is a multi-agent AI orchestration platform designed to automatically transform abstract innovation concepts into fully structured, production-ready proposals. Powered by a collaborative pipeline of specialized AI personas—including Inventors, Engineers, and Critics—the platform breaks down a raw idea, generates its technical architecture, runs economic validations, and produces an optimized business case. Built for performance and security, NovaForge bridges advanced agent workflows with standard system integrations via an engineered Model Context Protocol (MCP) layer.

---

# 🌐 Live Demo & Local Execution

🚀 **Repository Link:** [Click here to view the NovaForge AI Source Code](https://github.com/windlower4596-cyber/NovaForge)

- **Deployment Context:** Runs completely offline / locally for validation safety.
- **Zero Cloud Dependencies:** No complex cloud infrastructure, Docker containers, or external hosting setups required.

---

# 🚀 Overview
<img width="947" height="486" alt="Image" src="https://github.com/user-attachments/assets/73a78675-5fe6-4c42-aeb4-49649c27da7b" />

NovaForge addresses the limitations of single-prompt AI workflows by implementing a structured, collaborative multi-agent simulation. The platform divides complex goals into specialized sub-tasks managed by individual, role-specific agents. A centralized coordinator manages the execution sequence, routing data between agents and synthesizing their outputs into a final product. This mimics a real-world software engineering and product team, reducing hallucination rates and significantly increasing the logical depth of generated projects.

The system relies heavily on the Model Context Protocol (MCP) to provide agents with secure, standardized entry points to interact with the host system, manage databases, and execute localized scripting tools. Backed by a high-performance Python/FastAPI backend and a fast, modern React/Vite frontend, NovaForge brings visibility to agent interactions, allowing developers to monitor thoughts, criticisms, and iterations in real time.

## Platform Capabilities

- Multi-agent orchestration: Run pipelines where an Inventor, Engineer, Economist, and Critic collaborate on a single objective.
- Proposal generation: Automatically output clean Markdown proposals compiling all agent analyses.
- Patent brainstorming: Shape novel ideas with technical uniqueness checks.
- Cloud cost estimation: Calculate hosting and structural overhead costs.
- Security risk evaluation: Identify logical vulnerabilities and system threats.
- Markdown export: Compile output seamlessly for immediate file deployment.

---

# ✨ Key Features

## 🤖 Multi-Agent Workflow
<img width="955" height="488" alt="Image" src="https://github.com/user-attachments/assets/5929ca72-ba95-4ec1-9994-6da5af50ce2a" />

**Coordinator ➜ Inventor ➜ Engineer ➜ Economist ➜ Critic ➜ Pitch Generator**

### Centralized Coordination

Managed by a Coordinator agent that delegates tasks sequentially to sub-agents while maintaining global execution state.

### The Persona Pipeline

- **Inventor:** Generates initial concepts, algorithmic approaches, and novel core ideas.
- **Engineer:** Translates concepts into concrete implementation designs, directory layouts, and code structures.
- **Economist & Pitch Generator:** Produces commercial viability analysis, resource estimates, and business strategies.
- **Critic:** Evaluates structural weaknesses, security vulnerabilities, and logic flaws before the proposal is finalized.

---

## 🔌 Engine / API Architecture

- FastAPI REST endpoints for workflow execution and state tracking.
- MCP tool integration providing standardized system communication.
- SQLAlchemy ORM for persistent proposal and agent history storage.
- Pydantic validation enforcing strict request and response schemas.

---

# 🛡️ Security

- Prompt sanitization against instruction injection.
- Input validation using typed schemas.
- Typed request models via Pydantic.
- Backend isolation for secure tool execution.

---

# 🏗️ System Architecture

```text
Browser
   │
   ▼
React + Vite Frontend
   │
REST API
   │
   ▼
FastAPI Backend
   │
   ▼
Coordinator Agent
   │
 ├── Inventor
 ├── Engineer
 ├── Economist
 ├── Critic
 └── Pitch Generator
   │
   ▼
MCP Tools
   │
   ▼
SQLite Database
```

---

# 🛠️ Tech Stack

| Layer | Technologies |
|--------|--------------|
| Frontend | React, Vite |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Database | SQLite |
| Protocol | REST API, MCP |

---

# 📂 Project Structure

```text
NovaForge/
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── agents/           # Multi-agent workflow
│   │   ├── mcp/              # MCP client
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── requirements.txt
│   └── run.py
│
├── frontend/                 # React frontend
│   └── src/
│
├── cli.py                    # CLI execution
├── proposal_output.md        # Generated proposal output
├── start.bat                 # One-click startup
├── test_backend.py           # Backend tests
└── README.md
```

---

# ⚙️ Installation & Setup

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- npm

---

## 🚀 One-Click Execution (Recommended)

Clone the repository:

```bash
git clone https://github.com/windlower4596-cyber/NovaForge.git
cd NovaForge
```

Run:

```bash
start.bat
```

This automatically launches the backend, frontend, and supporting services.

Open:

```text
http://localhost:5173
```

---

# 🔮 Future Improvements

- [ ] Authentication
- [ ] Docker Compose
- [ ] CI/CD Pipeline
- [ ] Streaming Responses
- [ ] Kubernetes Deployment

---

## 👨‍💻 Author

**Ayush Singh**

## 📄 License

**MIT License**

---

> *Transforming ideas into production-ready innovation through collaborative AI agents.*

