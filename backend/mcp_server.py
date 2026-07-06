import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

app = FastAPI(
    title="NovaForge AI MCP Server",
    description="Offline Model Context Protocol Server providing specialized tools for multi-agent workflows.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define schemas for JSON-RPC MCP style communication
class MCPTool(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPToolResponse(BaseModel):
    tools: List[MCPTool]

class CallToolRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

class CallToolResponse(BaseModel):
    content: List[Dict[str, Any]]
    isError: bool = False

# Tool definitions
TOOLS = [
    MCPTool(
        name="brainstorm_patent_tags",
        description="Brainstorm relevant patent classifications and tags based on a technical innovation idea.",
        inputSchema={
            "type": "object",
            "properties": {
                "idea": {"type": "string", "description": "The technical innovation idea."}
            },
            "required": ["idea"]
        }
    ),
    MCPTool(
        name="estimate_cloud_cost",
        description="Calculate estimated hosting and operational cloud costs based on complexity and user scale.",
        inputSchema={
            "type": "object",
            "properties": {
                "complexity": {"type": "string", "enum": ["low", "medium", "high"], "description": "Project technical complexity."},
                "scale": {"type": "string", "enum": ["prototype", "smb", "enterprise"], "description": "Scale of deployment."}
            },
            "required": ["complexity", "scale"]
        }
    ),
    MCPTool(
        name="evaluate_security_risks",
        description="Check for common security risks, architectural bottlenecks, and OWASP issues based on selected technologies.",
        inputSchema={
            "type": "object",
            "properties": {
                "tech_stack": {"type": "array", "items": {"type": "string"}, "description": "List of technologies in the stack."}
            },
            "required": ["tech_stack"]
        }
    )
]

@app.get("/")
def read_root():
    return {"status": "online", "mcp": "Model Context Protocol Server is ready", "port": 8001}

@app.get("/tools", response_model=MCPToolResponse)
def list_tools():
    """
    List all available tools in the MCP Server.
    """
    return MCPToolResponse(tools=TOOLS)

@app.post("/tools/call", response_model=CallToolResponse)
def call_tool(request: CallToolRequest):
    """
    Execute a tool by name with arguments.
    """
    name = request.name
    args = request.arguments

    if name == "brainstorm_patent_tags":
        idea = args.get("idea", "")
        if not idea:
            return CallToolResponse(content=[{"type": "text", "text": "Error: missing 'idea' argument"}], isError=True)
        
        # Simple local heuristic for patent tagging
        idea_lower = idea.lower()
        tags = []
        classifications = []
        
        if any(w in idea_lower for w in ["solar", "power", "energy", "electricity"]):
            tags.extend(["Renewable Energy", "Photovoltaics", "Smart Grid", "Energy Storage"])
            classifications.extend(["H02S (Generation of electric power from solar energy)", "H02J (Circuit arrangements for energy storage)"])
        if any(w in idea_lower for w in ["lock", "security", "door", "safe", "access"]):
            tags.extend(["Smart Access Control", "Physical Security", "Biometrics", "IoT Security"])
            classifications.extend(["E05B (Locks/keys)", "G07C (Time/attendance, registration, access control)"])
        if any(w in idea_lower for w in ["smart", "iot", "sensor", "wireless", "device"]):
            tags.extend(["Internet of Things", "Sensor Network", "Embedded Systems", "Edge Computing"])
            classifications.extend(["G16Y (Information tech specially adapted for IoT)", "H04W (Wireless communication networks)"])
        if any(w in idea_lower for w in ["database", "data", "blockchain", "ai", "model", "learning"]):
            tags.extend(["Machine Learning", "Artificial Intelligence", "Data Engineering", "Neural Networks"])
            classifications.extend(["G06N (Computing arrangements using specific computational models)", "G06F 16/00 (Information retrieval)"])
            
        if not tags:
            tags = ["General Software System", "Distributed Computing"]
            classifications = ["G06F 15/00 (Digital computers in general)"]
            
        result_text = f"Suggested Patent Classifications:\n" + "\n".join(f"- {c}" for c in classifications) + \
                      f"\n\nSuggested Innovation Keywords: " + ", ".join(tags)
                      
        return CallToolResponse(content=[{"type": "text", "text": result_text}])

    elif name == "estimate_cloud_cost":
        complexity = args.get("complexity", "medium")
        scale = args.get("scale", "prototype")
        
        # Cost multipliers
        base_costs = {
            "prototype": {"compute": 15, "db": 10, "storage": 5, "bandwidth": 5},
            "smb": {"compute": 120, "db": 80, "storage": 40, "bandwidth": 30},
            "enterprise": {"compute": 850, "db": 600, "storage": 400, "bandwidth": 350}
        }
        
        mult = 1.0
        if complexity == "low":
            mult = 0.7
        elif complexity == "high":
            mult = 1.5
            
        costs = base_costs.get(scale, base_costs["prototype"])
        compute_est = int(costs["compute"] * mult)
        db_est = int(costs["db"] * mult)
        storage_est = int(costs["storage"] * mult)
        bandwidth_est = int(costs["bandwidth"] * mult)
        total = compute_est + db_est + storage_est + bandwidth_est
        
        result_text = (
            f"Monthly Cloud Infrastructure Cost Estimates ({scale.upper()} scale, {complexity.upper()} complexity):\n"
            f"- Compute Nodes (EC2/Fargate/GKE): ${compute_est}/month\n"
            f"- Managed Database (RDS/CloudSQL): ${db_est}/month\n"
            f"- Cloud Storage (S3/CloudStorage): ${storage_est}/month\n"
            f"- Bandwidth & CDN (CloudFront): ${bandwidth_est}/month\n"
            f"=========================================\n"
            f"Total Estimated Infrastructure Cost: ${total}/month"
        )
        return CallToolResponse(content=[{"type": "text", "text": result_text}])

    elif name == "evaluate_security_risks":
        tech_stack = args.get("tech_stack", [])
        if not tech_stack:
            return CallToolResponse(content=[{"type": "text", "text": "Error: missing 'tech_stack' argument"}], isError=True)
            
        risks = []
        for tech in tech_stack:
            t = tech.lower()
            if "react" in t or "javascript" in t or "frontend" in t:
                risks.append({
                    "tech": tech,
                    "threat": "Cross-Site Scripting (XSS) & Dependency Vulnerabilities",
                    "mitigation": "Sanitize inputs, implement strict Content Security Policy (CSP), run 'npm audit' weekly, and keep react-router/dependencies updated."
                })
            if "fastapi" in t or "python" in t or "backend" in t:
                risks.append({
                    "tech": tech,
                    "threat": "Data Leakage, Unhandled Exceptions, & CORS Misconfiguration",
                    "mitigation": "Disable default swagger docs in production if confidential, configure CORS origins restrictively, use Pydantic models for strict type validation."
                })
            if "sqlite" in t or "sql" in t or "database" in t:
                risks.append({
                    "tech": tech,
                    "threat": "SQL Injection & File Access Vulnerabilities",
                    "mitigation": "Use SQLAlchemy ORM parameterized queries exclusively. Secure the sqlite file access permissions."
                })
            if "iot" in t or "sensor" in t or "lock" in t or "hardware" in t:
                risks.append({
                    "tech": tech,
                    "threat": "Man-in-the-Middle (MITM) & Eavesdropping",
                    "mitigation": "Enforce SSL/TLS for all MQTT/HTTP communications. Store private keys in secure hardware modules (TPM/Secure Element)."
                })
                
        if not risks:
            risks.append({
                "tech": "Generic Stack",
                "threat": "Authentication & Authorization Flaws",
                "mitigation": "Implement role-based access control (RBAC), utilize HTTPS, and enforce strong password policies."
            })
            
        result_text = "Security Risk Analysis & Mitigations:\n\n"
        for idx, risk in enumerate(risks, 1):
            result_text += f"{idx}. Technology: {risk['tech']}\n"
            result_text += f"   - Threat: {risk['threat']}\n"
            result_text += f"   - Mitigation: {risk['mitigation']}\n\n"
            
        return CallToolResponse(content=[{"type": "text", "text": result_text}])

    else:
        return CallToolResponse(content=[{"type": "text", "text": f"Error: Tool '{name}' not found."}], isError=True)

if __name__ == "__main__":
    uvicorn.run("mcp_server:app", host="127.0.0.1", port=8001, reload=False)
