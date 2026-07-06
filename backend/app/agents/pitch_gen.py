from .base import BaseAgent
from typing import Dict, Any

class PitchGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Pitch Generator Agent",
            description="Compiles sections from all agents into a unified professional proposal pitch.",
            instruction="Organize and refine the collective output into an executive-ready proposal document."
        )

    def run(self, idea_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logs = []
        logs.append(f"[{self.name}] Gathering outputs from all specialist agents...")
        
        ctx = context or {}
        inventor_output = ctx.get("Inventor Agent", {}).get("output", "Invention details pending.")
        engineer_output = ctx.get("Engineer Agent", {}).get("output", "Engineering details pending.")
        economist_output = ctx.get("Economist Agent", {}).get("output", "Financial details pending.")
        critic_output = ctx.get("Critic Agent", {}).get("output", "Critic audit details pending.")
        
        logs.append(f"[{self.name}] Synthesizing Executive Summary...")
        logs.append(f"[{self.name}] Building Phase Deployment timeline...")

        exec_summary = (
            f"NovaForge AI is proud to present this comprehensive innovation proposal for **{idea_text}**. "
            f"By combining patent-grade novel claims, optimized backend and hardware schemas, "
            f"structured cloud budget allocations, and rigorous security threat mitigation, "
            f"this system stands ready for immediate prototype construction and market positioning."
        )

        timeline = (
            "| Phase | Timeline | Focus Area | Key Deliverables |\n"
            "|---|---|---|---|\n"
            "| **Phase 1** | Weeks 1-4 | Prototype & Firmware | Functional breadboard, basic local SQLite API endpoints. |\n"
            "| **Phase 2** | Weeks 5-8 | Cloud Integration | Standing up MCP-compliant tools, security hardening, CORS setup. |\n"
            "| **Phase 3** | Weeks 9-12 | Security Audit & Pilot | Complete external pentest, pilot deployment of 5 test devices. |"
        )

        # Build full markdown
        compiled_pitch = (
            f"# Innovation Proposal: {idea_text}\n\n"
            f"## SECTION 1: EXECUTIVE SUMMARY\n"
            f"{exec_summary}\n\n"
            f"---\n\n"
            f"## SECTION 2: PATENT & INNOVATION SCOPE\n"
            f"{inventor_output}\n\n"
            f"---\n\n"
            f"## SECTION 3: SYSTEM ARCHITECTURE & ENGINEERING\n"
            f"{engineer_output}\n\n"
            f"---\n\n"
            f"## SECTION 4: FINANCIAL MODEL & CLOUD COSTS\n"
            f"{economist_output}\n\n"
            f"---\n\n"
            f"## SECTION 5: SECURITY AUDIT & RISK PLAN\n"
            f"{critic_output}\n\n"
            f"---\n\n"
            f"## SECTION 6: PHASE DEPLOYMENT ROADMAP\n"
            f"{timeline}\n"
        )

        logs.append(f"[{self.name}] Completed compiling proposal.")
        
        return {
            "logs": "\n".join(logs),
            "output": compiled_pitch,
            "data": {
                "exec_summary": exec_summary,
                "timeline": timeline
            }
        }
