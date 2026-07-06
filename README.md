NovaForge AI 🚀
NovaForge AI is a multi-agent AI orchestration platform designed to automatically transform abstract innovation concepts into fully structured, production-ready proposals. Powered by a collaborative pipeline of specialized AI personas—including Inventors, Engineers, and Critics—the platform breaks down a raw idea, generates its technical architecture, runs economic validations, and produces an optimized business case. Built for performance and security, NovaForge bridges advanced agent workflows with standard system integrations via an engineered Model Context Protocol (MCP) layer.

🌐 Live Demo & Local Execution
🚀 Repository Link: Click here to view the NovaForge AI Source Code

Deployment Context: Runs completely offline / locally for validation safety.

Zero Cloud Dependencies: No complex cloud infrastructure, Docker containers, or external hosting setups required.

⚠️ Examiner Note: To run this platform live on your machine, please follow the quick 1-click execution steps inside the Installation section below.

🚀 Overview
NovaForge addresses the limitations of single-prompt AI workflows by implementing a structured, collaborative multi-agent simulation. The platform divides complex goals into specialized sub-tasks managed by individual, role-specific agents. A centralized coordinator manages the execution sequence, routing data between agents and synthesizing their outputs into a final product. This mimics a real-world software engineering and product team, reducing hallucination rates and significantly increasing the logical depth of generated projects.

The system relies heavily on the Model Context Protocol (MCP) to provide agents with secure, standardized entry points to interact with the host system, manage databases, and execute localized scripting tools. Backed by a high-performance Python/FastAPI backend and a fast, modern React/Vite frontend, NovaForge brings visibility to agent interactions, allowing developers to monitor thoughts, criticisms, and iterations in real time.

Platform capabilities
Multi-agent orchestration: Run pipelines where an Inventor, Engineer, Economist, and Critic collaborate on a single objective.

Proposal generation: Automatically output clean Markdown proposals compiling all agent analyses.

Patent brainstorming: Shape novel ideas with technical uniqueness checks.

Cloud cost estimation: Calculate hosting and structural overhead costs.

Security risk evaluation: Identify logical vulnerabilities and system threats.

Markdown export: Compile output seamlessly for immediate file deployment.

✨ Key Features
🤖 Multi-Agent Workflow
Coordinator -> Inventor -> Engineer -> Economist -> Critic -> Pitch Generator

Centralized Coordination: Managed by a Coordinator agent that delegates tasks sequentially to sub-agents and maintains global execution state.

The Persona Pipeline: * Inventor: Generates initial concepts, algorithmic approaches, and novel core ideas.

Engineer: Translates concepts into concrete implementation designs, directory layouts, and code structures.

Economist & Pitch Generator: Appends commercial viability, resource estimates, and high-impact marketing strategies.

Critic: Evaluates structural weaknesses, security vulnerabilities, and logic flaws, forcing a recursive refinement loop.

🔌 Engine / API Architecture
FastAPI REST Endpoints: Uses structured backend hooks to trigger workflows and track state queries.

MCP Tool Integration: Controlled system access executing standardized Model Context Protocol setups.

SQLAlchemy Persistence: Safely maps incoming pipeline arrays into historical databases.

Pydantic Validation: Strict payload constraints verifying system interactions conform to runtime rules.

🛡️ Security
Prompt sanitization: Protects models against instruction injection vectors.

Input validation: Validates incoming payloads to maintain strict schema boundaries.

Typed request models: Ensures all fields match programmatic types explicitly.

Backend isolation: Safeguards computational tools behind standardized environments.

🏗️ Architecture
Browser -> React UI -> FastAPI -> Coordinator Agent (Inventor, Engineer, Economist, Critic, Pitch Generator) -> MCP Tools -> SQLite Database

🛠️ Tech Stack
Frontend: React

Backend: FastAPI

ORM: SQLAlchemy

Validation: Pydantic

Database: SQLite

Protocol: REST + MCP

📂 Project Structure
NovaForge/

backend/ - FastAPI application layer containing agent engines

backend/app/agents/ - Multi-agent workflow definitions and configurations

backend/mcp/ - Model Context Protocol client configurations

backend/requirements.txt - Main Python dependency list for backend libraries

frontend/ - Client-side modern reactive user interface

frontend/src/ - React dashboard pages, components, and styling assets

cli.py - Terminal tool script to trigger agent runs locally

proposal_output.md - Export file where final multi-agent proposals are saved

start.bat - Windows batch execution script to boot up the platform

test_backend.py - Automated unit testing suite validating backend APIs

⚙️ Installation & Setup
📋 Prerequisites
Before running the application, please ensure you have the following installed on your system:

Python 3.10+

Node.js (v18+) & npm

🚀 1-Click Execution Method (Recommended for Examiners)
Clone the repository to your local machine:
Run git clone https://github.com/windlower4596-cyber/NovaForge.git then cd NovaForge

Double-click the startup script located in the root directory:
Run start.bat
This will automatically open the required terminal windows, launch your background backend services, start up your frontend dev environment, and link them up instantly.

Access the application dashboard:
Open your web browser and click the link below to open the interface:

👉 http://localhost:5173

🔮 Future Improvements
[ ] Authentication

[ ] Docker Compose

[ ] CI/CD

[ ] Streaming responses

[ ] Kubernetes deployment

Author: AYUSH SINGH

License: MIT

Transforming ideas into production-ready innovation through collaborative AI agents.






*Transforming ideas into production-ready innovation through collaborative AI agents.*

