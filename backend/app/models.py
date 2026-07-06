import uuid
import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    idea_text = Column(Text, nullable=False)
    status = Column(String(50), default="processing")  # processing, completed, failed
    final_proposal = Column(Text, nullable=True)        # JSON string containing all completed sections
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship to agent logs
    logs = relationship("AgentLog", back_populates="proposal", cascade="all, delete-orphan")

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    proposal_id = Column(String(36), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(String(100), nullable=False)   # Coordinator, Inventor, Engineer, Economist, Critic, Pitch Generator
    status = Column(String(50), default="running")      # running, completed, failed
    logs = Column(Text, nullable=True)                  # Internal logs/thinking of the agent
    output = Column(Text, nullable=True)                # Actual content produced by the agent
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    proposal = relationship("Proposal", back_populates="logs")
