from .base import BaseAgent
from ..mcp.client import call_mcp_tool
from typing import Dict, Any

class InventorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Inventor Agent",
            description="Brainstorms technical novelty, core invention mechanism, and patent tags.",
            instruction="Focus on the uniqueness of the idea, core innovation layers, and patentable concepts."
        )

    def run(self, idea_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logs = []
        logs.append(f"[{self.name}] Initiated patent & novelty analysis for idea: '{idea_text}'")
        logs.append(f"[{self.name}] Scanning intellectual property classifications...")
        
        # Call MCP Tool
        mcp_patent_output = call_mcp_tool("brainstorm_patent_tags", {"idea": idea_text})
        logs.append(f"[{self.name}] Successfully fetched patent classifications from MCP Server.")
        logs.append(f"[{self.name}] Synthesizing invention core mechanisms...")

        # Construct simulated technical proposal content based on keywords
        idea_lower = idea_text.lower()
        novelty_points = []
        core_mechanism = ""
        
        if "solar" in idea_lower or "power" in idea_lower or "energy" in idea_lower:
            novelty_points = [
                "Self-sustaining power harvesting system using integrated micro-photovoltaic cells.",
                "Dynamic energy throttling algorithm that slows down non-essential IoT routines during low sunlight.",
                "High-efficiency trickle charge controller protecting local solid-state battery reserves."
            ]
            core_mechanism = (
                "An intelligent micro-solar panel collects ambient light, converting it to DC current. "
                "The energy is fed into a charge controller that implements maximum power point tracking (MPPT) at a micro-scale. "
                "Hardware signals send energy states to the edge microcontroller, enabling adaptive hibernation cycles."
            )
        elif "lock" in idea_lower or "security" in idea_lower or "door" in idea_lower:
            novelty_points = [
                "Cryptographic physical handshake protocol using dynamic NFC and bluetooth low energy (BLE).",
                "Biometric pattern matching executing exclusively within a secure enclave to prevent network spoofing.",
                "Autonomous mechanical torque override that automatically seals entry-points in high-risk scenarios."
            ]
            core_mechanism = (
                "The lock remains in deep sleep until an NFC trigger wake-up pulse is detected. "
                "Once awake, it conducts a zero-knowledge proof verification with the user's mobile secure element. "
                "Upon validation, a brushless DC motor activates a high-torque mechanical deadbolt mechanism."
            )
        else:
            novelty_points = [
                "Distributed consensus routing of local events using low-power edge nodes.",
                "Self-correcting data telemetry queue which compresses payloads during poor signal states.",
                "Zero-trust secure API architecture utilizing localized cryptographic device certificates."
            ]
            core_mechanism = (
                "The software system runs a lightweight telemetry listener daemon. "
                "Events are serialized using Protocol Buffers to minimize transport size, "
                "then routed via an asynchronous queue with automated exponential back-off and retry logic."
            )

        output_md = (
            f"### Patent & Novelty Report: {idea_text[:40]}...\n\n"
            f"#### 1. Core Invention Mechanism\n"
            f"{core_mechanism}\n\n"
            f"#### 2. Key Novelty Claims\n"
            f"- **Claim 1 (Autonomous Operation):** {novelty_points[0]}\n"
            f"- **Claim 2 (Efficiency Optimization):** {novelty_points[1]}\n"
            f"- **Claim 3 (Secured Enclave):** {novelty_points[2]}\n\n"
            f"#### 3. Patent Classifications & Tags\n"
            f"{mcp_patent_output}\n"
        )

        return {
            "logs": "\n".join(logs),
            "output": output_md,
            "data": {
                "novelty_points": novelty_points,
                "core_mechanism": core_mechanism,
                "patent_tags": mcp_patent_output
            }
        }
