import json
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db, Base
from .models import Proposal, AgentLog
from .schemas import ProposalCreate, ProposalResponse, ProposalDetailResponse
from .security import validate_user_idea
from .agents import CoordinatorAgent

# Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NovaForge AI Backend API",
    description="Backend services for the NovaForge AI multi-agent orchestration engine.",
    version="1.0.0"
)

# Enable CORS for frontend web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app runs on localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = CoordinatorAgent()

@app.get("/")
def health_check():
    return {"status": "online", "service": "NovaForge AI Backend Server", "port": 8000}

@app.post("/api/v1/proposals", response_model=ProposalResponse, status_code=status.HTTP_201_CREATED)
def create_proposal(payload: ProposalCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Validate idea, create database placeholder, and start the multi-agent orchestration in background.
    """
    # 1. Validation & Sanitization (Security Features)
    validated_idea = validate_user_idea(payload.idea_text)
    
    # 2. Database record
    proposal = Proposal(
        title="Processing...",
        idea_text=validated_idea,
        status="processing"
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)

    # 3. Trigger asynchronous multi-agent coordination
    background_tasks.add_task(coordinator.execute_workflow, proposal.id)

    return proposal

@app.get("/api/v1/proposals", response_model=List[ProposalResponse])
def get_proposals(db: Session = Depends(get_db)):
    """
    List all proposals ordered by creation date.
    """
    return db.query(Proposal).order_by(Proposal.created_at.desc()).all()

@app.get("/api/v1/proposals/{proposal_id}", response_model=ProposalDetailResponse)
def get_proposal_detail(proposal_id: str, db: Session = Depends(get_db)):
    """
    Retrieve full details of a proposal, including deserialized sections and agent logs.
    """
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    # Construct detail response manually to handle JSON parsing
    logs = db.query(AgentLog).filter(AgentLog.proposal_id == proposal_id).order_by(AgentLog.created_at.asc()).all()
    
    final_proposal_dict = None
    if proposal.final_proposal:
        try:
            final_proposal_dict = json.loads(proposal.final_proposal)
        except Exception:
            final_proposal_dict = {"pitch": proposal.final_proposal}

    return ProposalDetailResponse(
        id=proposal.id,
        title=proposal.title,
        idea_text=proposal.idea_text,
        status=proposal.status,
        created_at=proposal.created_at,
        final_proposal=final_proposal_dict,
        logs=logs
    )

@app.delete("/api/v1/proposals/{proposal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_proposal(proposal_id: str, db: Session = Depends(get_db)):
    """
    Delete a proposal and all its linked agent logs.
    """
    proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
        
    db.delete(proposal)
    db.commit()
    return None
