from .base import BaseAgent
from ..mcp.client import call_mcp_tool
from typing import Dict, Any

class EconomistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Economist Agent",
            description="Computes cloud server estimates, overall budget, ROI, and commercialization models.",
            instruction="Focus on financial sustainability, cloud costs, and ROI projection models."
        )

    def run(self, idea_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        logs = []
        logs.append(f"[{self.name}] Assessing engineering specifications...")
        
        engineer_data = (context or {}).get("Engineer Agent", {}).get("data", {})
        tech_stack = engineer_data.get("tech_stack", [])
        
        logs.append(f"[{self.name}] Querying MCP Server for cloud infrastructure costs...")
        
        # Decide complexity and scale
        complexity = "medium"
        if len(tech_stack) > 5:
            complexity = "high"
        elif len(tech_stack) < 3:
            complexity = "low"
            
        mcp_cost_output_prototype = call_mcp_tool("estimate_cloud_cost", {"complexity": complexity, "scale": "prototype"})
        mcp_cost_output_production = call_mcp_tool("estimate_cloud_cost", {"complexity": complexity, "scale": "smb"})
        
        logs.append(f"[{self.name}] Received estimated cloud costs.")
        logs.append(f"[{self.name}] Formulating investment projections and revenue models...")

        # Calculate estimated developmental ROI
        initial_development_budget = 45000 if complexity == "low" else 85000 if complexity == "medium" else 150000
        estimated_market_value = initial_development_budget * 2.5
        roi_percentage = int(((estimated_market_value - initial_development_budget) / initial_development_budget) * 100)

        output_md = (
            f"### Financial Projection & Feasibility Analysis\n\n"
            f"#### 1. Estimated Cloud Infrastructure Budget\n"
            f"##### A. Prototype Stage (First 6 months)\n"
            f"```text\n"
            f"{mcp_cost_output_prototype}\n"
            f"```\n\n"
            f"##### B. Commercial/Scale Stage (Post-launch)\n"
            f"```text\n"
            f"{mcp_cost_output_production}\n"
            f"```\n\n"
            f"#### 2. Developmental Cost Breakdown\n"
            f"- **Personnel (Engineering, Design, QA):** ${int(initial_development_budget * 0.70):,}\n"
            f"- **Legal, Patents, and Licensing:** ${int(initial_development_budget * 0.15):,}\n"
            f"- **Hardware Prototyping & Equipment:** ${int(initial_development_budget * 0.10):,}\n"
            f"- **Contingency Buffer:** ${int(initial_development_budget * 0.05):,}\n"
            f"- **Total Initial Development Budget:** **${initial_development_budget:,}**\n\n"
            f"#### 3. Monetization Strategy & ROI\n"
            f"- **Monetization Model:** B2B SaaS licensing + Hardware/IoT setup fee (if hardware-related).\n"
            f"- **Estimated 1-Year Valuation:** ${int(estimated_market_value):,}\n"
            f"- **Projected Net ROI:** **{roi_percentage}%**\n"
            f"- **Break-Even Analysis:** 14 months post-launch based on securing 15 active enterprise clients."
        )

        return {
            "logs": "\n".join(logs),
            "output": output_md,
            "data": {
                "initial_development_budget": initial_development_budget,
                "roi_percentage": roi_percentage,
                "monthly_cloud_costs_prototype": mcp_cost_output_prototype
            }
        }
