import time
import json
import logging
from sqlalchemy.orm import Session
from ..models import Proposal, AgentLog
from .inventor import InventorAgent
from .engineer import EngineerAgent
from .economist import EconomistAgent
from .critic import CriticAgent
from .pitch_gen import PitchGeneratorAgent

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    def __init__(self):
        self.agents = [
            InventorAgent(),
            EngineerAgent(),
            EconomistAgent(),
            CriticAgent(),
            PitchGeneratorAgent()
        ]

    def execute_workflow(self, proposal_id: str):
        """
        Runs the multi-agent system sequentially.
        Writes all agent reasoning logs and outputs to the SQLite database.
        """
        from ..database import SessionLocal

        db = SessionLocal()
        try:
            # Fetch the proposal from the DB
            proposal = db.query(Proposal).filter(Proposal.id == proposal_id).first()
            if not proposal:
                logger.error(f"Proposal {proposal_id} not found in database.")
                return

            proposal.status = "processing"
            db.commit()

            context = {}
            
            try:
                for agent in self.agents:
                    # 1. Create a log entry for this agent
                    agent_log = AgentLog(
                        proposal_id=proposal.id,
                        agent_name=agent.name,
                        status="running",
                        logs=f"[{agent.name}] Initializing reasoning sequence..."
                    )
                    db.add(agent_log)
                    db.commit()

                    # Add a tiny delay to simulate realistic agent coordination
                    time.sleep(1.0)

                    try:
                        # 2. Run agent reasoning
                        result = agent.run(proposal.idea_text, context)
                        
                        # 3. Save outcomes
                        agent_log.status = "completed"
                        agent_log.logs = result.get("logs", "")
                        agent_log.output = result.get("output", "")
                        db.commit()

                        # Add to context
                        context[agent.name] = result
                    except Exception as e:
                        agent_log.status = "failed"
                        agent_log.logs = f"Error during agent execution: {str(e)}"
                        db.commit()
                        raise e

                # Synthesize final document
                pitch_data = context.get("Pitch Generator Agent", {})
                final_md = pitch_data.get("output", "")

                # Structuring the sections for easy frontend rendering
                proposal_dict = {
                    "inventor": context.get("Inventor Agent", {}).get("output", ""),
                    "engineer": context.get("Engineer Agent", {}).get("output", ""),
                    "economist": context.get("Economist Agent", {}).get("output", ""),
                    "critic": context.get("Critic Agent", {}).get("output", ""),
                    "pitch": final_md
                }

                # Extrapolate a title
                title_words = proposal.idea_text.split()
                title = " ".join(title_words[:4]) + " Project"
                if len(title) > 60:
                    title = title[:57] + "..."

                # Save the final results to DB
                proposal.title = title
                proposal.final_proposal = json.dumps(proposal_dict)
                proposal.status = "completed"
                db.commit()

                logger.info(f"Proposal {proposal_id} workflow successfully completed.")

            except Exception as e:
                logger.exception(f"Error during proposal {proposal_id} orchestration:")
                proposal.status = "failed"
                db.commit()
        finally:
            db.close()
