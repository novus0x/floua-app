########## Modules ##########
import re

from datetime import datetime
from typing import Dict, List

from sqlalchemy.orm import Session

from db.model import User, Concept_Network, Learning_Experience

from core.utils.generator import get_uuid
from core.utils.db_management import add_db

########## Reasoning ##########
class Reasoning:
    def __init__(self):
        self.reasoning_methods = {
            "deductive": self._deductive_reasoning,
            "inductive": self._inductive_reasoning,
            "abductive": self._abductive_reasoning,
            "analogical": self._analogical_reasoning            
        }

    def reason_about_query(self, db: Session, query: str, context: Dict = None):
        query_analysis = self._analyze_query(query)
        reasoning_method = self._select_reasoning_method(query_analysis)
        reasoning_result = self.reasoning_methods[reasoning_method](
            db, query, query_analysis, context
        )

        return {
            "reasoning_method": reasoning_method,
            "reasoning_steps": reasoning_result["steps"],
            "conclusion": reasoning_result["conclusion"],
            "confidence": reasoning_result["confidence"]
        }

    def _analyze_query(self, query: str):
        analysis = {
            "query_type": "unknown",
            "concepts": [],
            "relationships": [],
            "intent": "unknown"
        }

        if any(word in query.lower() for word in ["what is", "what are", "define"]):
            analysis["query_type"] = "definition"
        elif any(word in query.lower() for word in ["how to", "how do i"]):
            analysis["query_type"] = "procedure"
        elif any(word in query.lower() for word in ["why", "because"]):
            analysis["query_type"] = "causality"
        elif "?" in query:
            analysis["query_type"] = "question"
        
        words = re.findall(r"\b\w+\b", query.lower())
        analysis["concepts"] = [word for word in words if len(word) > 3]

        return analysis

    def _select_reasoning_method(self, query_analysis: Dict):
        query_type = query_analysis["query_type"]

        method_mad = {
            "definition": "deductive",
            "procedure": "deductive",
            "causality": "abductive",
            "question": "inductive"
        }

        return method_mad.get(query_type, "inductive")

    def _deductive_reasoning(self, db: Session, query: str, analysis: Dict, context: Dict):
        steps = []
        conclusion = None
        confidence = 0.0

        concepts = analysis["concepts"]

        for concept in concepts:
            concept_data = db.query(Concept_Network).filter(
                Concept_Network.concept_name == concept
            ).first()

            if concept_data:
                steps.append(f"Concept found: {concept}")

                if concept_data.concept_definition:
                    conclusion = concept_data.concept_definition
                    confidence = concept_data.confidence
                    steps.append(f"Applied definition: {conclusion}")

                    break
        
        return {
            "steps": steps,
            "conclusion": conclusion,
            "confidence": confidence
        }
    
    def _inductive_reasoning(self, db: Session, query: str, analysis: Dict, context: Dict):
        steps = ["Searching for previous patterns"]

        similar_experience = db.query(Learning_Experience).filter(
            Learning_Experience.input_data.like(f"%{analysis["concepts"][0]}%")
        ).all() if analysis["concepts"] else []

        conclusion = "Based on previous experiences, I can infer that..."
        confidence = 0.6

        if similar_experience:
            conclusion = min(0.8, 0.6 + len(similar_experience) * 0.1)

        return {
            "steps": steps,
            "conclusion": conclusion,
            "confidence": confidence
        }

    def _abductive_reasoning(self, db: Session, query: str, analysis: Dict, context: Dict):
        steps = ["Looking for the most likely explanation..."]

        conclusion = "Based on available information, the most plausible explanation is..."
        confidence = 0.5

        return {
            "steps": steps,
            "conclusion": conclusion,
            "confidence": confidence
        }

    def _analogical_reasoning(self, db: Session, query: str, analysis: Dict, context: Dict):
        steps = ["Searching for similar patterns of analogies..."]

        conclusion = "This reminds me of similar patterns I've encountered..."
        confidence = 0.4

        return {
            "steps": steps,
            "conclusion": conclusion,
            "confidence": confidence
        }
