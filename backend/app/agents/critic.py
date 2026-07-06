from .base import BaseAgent
from ..mcp.client import call_mcp_tool
from typing import Dict, Any

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Critic Agent",
            description="Reviews proposals, runs SWOT reviews, identifies security risks, and suggests mitigations.",
            instruction="Be objective and critical. Focus on security threats, bottlenecks, and engineering constraints."
        )

    def run(self, idea_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logs = []
        logs.append(f"[{self.name}] Initiating independent audit of engineering and financial components...")
        
        engineer_data = (context or {}).get("Engineer Agent", {}).get("data", {})
        tech_stack = engineer_data.get("tech_stack", [])
        
        logs.append(f"[{self.name}] Querying MCP security tool for stack scan: {tech_stack}...")
        
        # Call MCP Tool
        mcp_security_output = call_mcp_tool("evaluate_security_risks", {"tech_stack": tech_stack})
        
        logs.append(f"[{self.name}] Security scan returned recommendations.")
        logs.append(f"[{self.name}] Drafting SWOT matrix and risk log...")

        # Construct SWOT based on keywords
        idea_lower = idea_text.lower()
        if "solar" in idea_lower or "power" in idea_lower or "energy" in idea_lower:
            swot = (
                "| **Strengths** | **Weaknesses** |\n"
                "|---|---|\n"
                "| - Energy independence<br>- Green tech footprint | - Weather dependency<br>- High initial hardware setup cost |\n"
                "| **Opportunities** | **Threats** |\n"
                "|---|---|\n"
                "| - Carbon credit eligibility<br>- Micro-grid integrations | - Theft of solar devices<br>- Battery degradation over 5 years |"
            )
            bottleneck = "Micro-solar panel efficiency drop in low light and extreme temperatures."
        elif "lock" in idea_lower or "security" in idea_lower:
            swot = (
                "| **Strengths** | **Weaknesses** |\n"
                "|---|---|\n"
                "| - Biometric hardware enclave<br>- Offline zero-knowledge locks | - Power failure locks user out<br>- Firmware upgrade complexities |\n"
                "| **Opportunities** | **Threats** |\n"
                "|---|---|\n"
                "| - Smart-home ecosystems<br>- Enterprise physical security integration | - Wireless spoofing attacks<br>- Lock picking or brute physical force |"
            )
            bottleneck = "Securing cryptographic keys locally in the microcontroller enclave without increasing device wake-up times."
        else:
            swot = (
                "| **Strengths** | **Weaknesses** |\n"
                "|---|---|\n"
                "| - Highly modular endpoints<br>- SQLite concurrency optimization | - Heavy reliance on local hosting resources<br>- Missing geo-replication |\n"
                "| **Opportunities** | **Threats** |\n"
                "|---|---|\n"
                "| - Rapid containerization (Docker)<br>- Integration into larger microservices | - Dynamic security threats & API exploitation<br>- Scale limits of single-server instances |"
            )
            bottleneck = "CORS issues and database locking if multiple concurrent write operations exceed SQLite capacity."

        output_md = (
            f"### Security Audit & Constructive Critique\n\n"
            f"#### 1. SWOT Analysis Matrix\n"
            f"{swot}\n\n"
            f"#### 2. Key Technical Bottlenecks\n"
            f"- **Primary Bottleneck:** {bottleneck}\n"
            f"- **System Vulnerability:** High CPU cycles if encryption algorithms are run without specialized low-power edge math hardware modules.\n\n"
            f"#### 3. MCP Security Risks Scan Results\n"
            f"```text\n"
            f"{mcp_security_output}\n"
            f"```\n"
            f"#### 4. Audit Verdict\n"
            f"**CONDITIONAL APPROVAL.** The engineering proposal is solid, provided that all mitigations identified by the security scan are implemented in the Phase-1 prototype."
        )

        return {
            "logs": "\n".join(logs),
            "output": output_md,
            "data": {
                "swot": swot,
                "bottleneck": bottleneck,
                "security_scan": mcp_security_output
            }
        }
