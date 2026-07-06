from .base import BaseAgent
from typing import Dict, Any

class EngineerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Engineer Agent",
            description="Designs system architecture, tech stack, database models, and REST API endpoints.",
            instruction="Provide practical, modular, and secure software and hardware architectural designs."
        )

    def run(self, idea_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logs = []
        logs.append(f"[{self.name}] Analyzing Inventor's patent specifications...")
        
        inventor_data = (context or {}).get("Inventor Agent", {}).get("data", {})
        core_mechanism = inventor_data.get("core_mechanism", "Core telemetry ingestion system.")
        
        logs.append(f"[{self.name}] Formulating system architecture design...")
        logs.append(f"[{self.name}] Defining database schema models and endpoints...")

        # Determine tech stack based on keywords
        idea_lower = idea_text.lower()
        if "solar" in idea_lower or "lock" in idea_lower or "iot" in idea_lower:
            tech_stack = ["Embedded C++", "FreeRTOS", "FastAPI (Python)", "SQLite", "MQTT Broker", "React + Tailwind"]
            db_schema = (
                "Table `DeviceLogs`:\n"
                "  - `id`: UUID (Primary Key)\n"
                "  - `device_id`: VARCHAR(100) (Indexed)\n"
                "  - `battery_level`: FLOAT\n"
                "  - `power_source`: VARCHAR(50)\n"
                "  - `lock_state`: VARCHAR(20)\n"
                "  - `timestamp`: DATETIME"
            )
            api_endpoints = (
                "- `POST /api/v1/devices/telemetry`: Ingests energy and lock status.\n"
                "- `POST /api/v1/devices/command`: Dispatches lock/unlock signals to target hardware.\n"
                "- `GET /api/v1/devices/{device_id}/status`: Retrieves latest device telemetry state."
            )
        else:
            tech_stack = ["FastAPI (Python)", "PostgreSQL", "React + Tailwind", "Docker", "Redis", "Celery Task Queue"]
            db_schema = (
                "Table `Users`:\n"
                "  - `id`: UUID (Primary key)\n"
                "  - `email`: VARCHAR(255) (Unique, Indexed)\n"
                "  - `hashed_password`: VARCHAR(255)\n\n"
                "Table `Transactions`:\n"
                "  - `id`: UUID (Primary Key)\n"
                "  - `user_id`: UUID (Foreign Key)\n"
                "  - `amount`: DECIMAL(10,2)\n"
                "  - `status`: VARCHAR(50)"
            )
            api_endpoints = (
                "- `POST /api/v1/auth/token`: Logs in users and returns JWT tokens.\n"
                "- `POST /api/v1/proposals`: Creates a new system resource.\n"
                "- `GET /api/v1/proposals/{id}`: Fetches details of a compiled proposal."
            )

        tech_list_str = ", ".join(tech_stack)
        output_md = (
            f"### Technical Architecture & Engineering Specifications\n\n"
            f"#### 1. System Technology Stack\n"
            f"- **Frontend:** React.js, Tailwind CSS (Vite build system)\n"
            f"- **Backend:** FastAPI (Python 3.11), Uvicorn server\n"
            f"- **Database:** SQLite (WAL mode enabled) / SQLAlchemy ORM\n"
            f"- **Hardware/Communication:** {tech_list_str}\n\n"
            f"#### 2. Database Models Schema Design\n"
            f"```sql\n"
            f"{db_schema}\n"
            f"```\n\n"
            f"#### 3. Core REST API Endpoints\n"
            f"{api_endpoints}\n\n"
            f"#### 4. Architecture Data Flow\n"
            f"The application routes frontend actions to the FastAPI backend over HTTP. "
            f"For telemetry ingestion, the system utilizes raw socket listeners or MQTT endpoints, "
            f"writing events asynchronously into SQLite. The data is retrieved using parameterized SQL queries "
            f"via SQLAlchemy to prevent SQL injection."
        )

        return {
            "logs": "\n".join(logs),
            "output": output_md,
            "data": {
                "tech_stack": tech_stack,
                "db_schema": db_schema,
                "api_endpoints": api_endpoints
            }
        }
