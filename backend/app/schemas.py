from pydantic import BaseModel, Field, constr
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProposalCreate(BaseModel):
    # Enforce safe length limits (10 to 2000 chars)
    idea_text: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="The innovation idea to process into a proposal."
    )

class AgentLogResponse(BaseModel):
    id: int
    proposal_id: str
    agent_name: str
    status: str
    logs: Optional[str]
    output: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ProposalResponse(BaseModel):
    id: str
    title: str
    idea_text: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProposalDetailResponse(ProposalResponse):
    final_proposal: Optional[Dict[str, Any]] = None  # Deserialized final proposal JSON
    logs: List[AgentLogResponse] = []

    class Config:
        from_attributes = True
        # Allow loading JSON strings as dicts in Pydantic serialization
