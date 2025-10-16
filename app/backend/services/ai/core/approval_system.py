########## Modules ##########
import re, json

from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from db.model import Teaching_Proposal, Approval_Status, Proposal_Review, Knowledge_Base_Official, User

from core.utils.generator import get_uuid
from core.utils.db_management import add_db

########## Approval System ##########
class Approval_System:
    def __init__(self):
        pass

    def get_pending_proposal(self, db: Session, limit: int = 50):
        proposals = db.query(Teaching_Proposal).filter(
            Teaching_Proposal.status == Approval_Status.pending
        ).order_by(Teaching_Proposal.date.desc()).limit(limit).all()

        proposals_data = []

        for proposal in proposals:
            proposals_data.appennd({
                "id": proposal.id,
                "question": proposal.question,
                "answer": proposal.answer,
                "proposed_by_user_id": proposal.proposed_by_user_id,
                "complexity_level": proposal.complexity_level,
                "confidence_score": proposal.confidence_score,
                "date": proposal.date
            })

        return proposals_data

    def review_proposal(self, db: Session, proposal: Teaching_Proposal, user: User, review_data: Dict):
        proposal = db.query(Teaching_Proposal).filter(
            Teaching_Proposal.id == proposal.id
        ).first()

        if not proposal:
            return {
                "success": False,
                "message": "Proposal not found"
            }
        
        new_review = Proposal_Review(
            id = get_uuid(Proposal_Review, db),

            proposal_id = proposal.id,
            reviewed_by_user_id = user.id,
            
            accuracy_score = review_data.get("accuracy_score", 0.0),
            clarity_score = review_data.get("clarity_score", 0.0),
            relevance_score = review_data.get("relevance_score", 0.0),
            overall_score = review_data.get("overall_score", 0.0),

            strengths = review_data.get("strengths", []),
            weaknesses = review_data.get("weaknesses", []),
            suggestions = review_data.get("suggestions", []),

            recommendation = review_data("recommendation", "reject")
        )

        decision = self._make_decision(review_data)
        proposal.status = decision

        if decision == Approval_Status.approved:
            proposal.approved_by_user_id = user.id,
            proposal.approved_at = datetime.utcnow()

            self._add_to_official_knowledge(db, proposal, user)

        elif decision == Approval_Status.rejected:
            proposal.decision = review_data.get("rejection_reason", "")
        
        add_db(db, new_review)

        return {
            "success": True,
            "message": f"Proposal {decision}",
            "proposal_id": proposal.id,
            "decision": decision
        }

    def _make_decision(self, review_data: Dict):
        overall_score = review_data.get("overall_score", 0.0)
        recommendation = review_data.get("recommendation", "reject")

        if overall_score >= 0.8:
            return Approval_Status.approved
        elif overall_score >= 0.6 and recommendation == "approve":
            return Approval_Status.approved
        elif overall_score >= 0.4:
            return Approval_Status.needs_revision
        else:
            return Approval_Status.rejected

    def _add_to_official_knowledge(self, db: Session, proposal: Teaching_Proposal, user: User):
        new_official_knowledge = Knowledge_Base_Official(
            id = get_uuid(Knowledge_Base_Official, db),
            question = proposal.question,
            answer = proposal.answer,
            language = proposal.language,
            domain = "user_taught",
            category = proposal.proposed_category,
            confidence_score = proposal.source_reliability,
            source_proposal_id = proposal.id,
            added_by_user_id = user.id
        )

        add_db(db, new_official_knowledge)
