########## Modules ##########
import re, json

from datetime import datetime
from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from db.model import Teaching_Proposal, Approval_Status, User,User_Role, Knowledge_Base_Official

from core.utils.generator import get_uuid
from core.utils.db_management import add_db

########## Variables ##########
ALLOWED_TEACHING_ROLES = [User_Role.admin, User_Role.moderator]

########## Controlled Teaching Interface ##########
class Controlled_Teaching_Interface:
    def __init__(self):
        pass

    def process_teaching_command(self, db: Session, command: str, user: User):
        teaching_data = self._parse_teaching_command(command)

        if not teaching_data:
            return {
                "success": False,
                "message": "Incorrect format. Use /teach [question] | [answer]"
            }

        new_proposal = Teaching_Proposal(
            id = get_uuid(Teaching_Proposal, db),
            question = teaching_data["question"],
            proposed_answer = teaching_data["answer"],
            language = "en",
            proposed_by_user_id = user.id,
        )

        self._analyze_proposal(new_proposal)
        add_db(new_proposal)

        if user.role in ALLOWED_TEACHING_ROLES:
            message = "Teaching proposal added and auto-approved (privileged role)"
            self._auto_approve_proposal(db, new_proposal, user)
        
        else:
            message = "Teaching proposal sent for approval. Moderators will review it soon."

        return {
            "success": True,
            "message": message,
            "proposal_id": new_proposal.id,
            "status": new_proposal.status
        }

    def _parse_teaching_command(self, command: str):
        clean_command = command.replace("/teach", "").strip()

        parts = clean_command.split("|", 1)

        if len(parts) != 2:
            return None

        question = parts[0].strip()
        answer = parts[1].strip()

        if not question or not answer:
            return None

        return {
            "question": question,
            "answer": answer
        }

    def _analyze_proposal(self, proposal: Teaching_Proposal):
        questions_words = len(proposal.question.split())
        answer_words = len(proposal.answer.split())

        if question_words <= 5 and answer_words <= 10:
            proposal.complexity_level = 1
        elif question_words <= 10 and answer_words <= 20:
            proposal.complexity_level = 2
        else:
            proposal.complexity_level = 3
            
        if len(proposal.answer) > 10 and "?" not in proposal.answer:
            proposal.source_reliability = 0.7
        else:
            proposal.source_reliability = 0.4

    def _auto_approve_proposal(self, db: Session, proposal: Teaching_Proposal, user: User):
        proposal = db.query(Teaching_Proposal).filter(
            Teaching_Proposal.id == proposal.id
        ).first()

        if proposal:
            proposal.status = Approval_Status.approved
            proposal.approved_by_user_id = user.id,
            proposal.approved_at = datetime.utcnow()

            new_official_knowledge = Knowledge_Base_Official(
                question = proposal.question,
                answer = proposal.answer,
                language = proposal.language,
                domain = "user_taught",
                confidence_score = proposal.source_reliability,
                source_proposal_id = proposal.id,
                added_by_user_id = user.id
            )

            add_db(new_official_knowledge, db)
