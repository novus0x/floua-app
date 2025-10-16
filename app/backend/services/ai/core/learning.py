########## Modules ##########
import re

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from db.model import Learning_Experience, Learning_Strategy, Concept_Network

from core.utils.generator import get_uuid
from core.utils.db_management import add_db

########## Autonomous Learning ##########
class Autonomous_Learning:
    def __init__(self):
        self.learning_strategies = {
            "pattern_recognition": self._learn_from_patterns,
            "concept_extraction": self._extract_concepts,
            "relationship_building": self._build_relationships,
            "gap_analysis": self._analyze_knowledge_gaps,
        }

    def process_learning_experience(self, db: Session, input_data: str, input_type: str, source: str):
        new_experience = Learning_Experience(
            id = get_uuid(Learning_Experience, db),
            input_data = input_data,
            input_type = input_type,
            source = source,
            learning_strategy = Learning_Strategy.active            
        )

        concepts = self._extract_concepts(input_data)
        patterns = self._learn_from_patterns(input_data)
        relationships = self._build_relationships(concepts)
        gaps = self._analyze_knowledge_gaps(concepts)

        new_experience.concept_extracted = concepts
        new_experience.knowledge_gaps_found = gaps
        new_experience.new_knowledge_created = len(concepts) > 0

        add_db(db, new_experience)

        self.update_concept_network(db, concepts)

        return {
            "success": True,
            "concepts_learned": concepts,
            "patterns_recognized": patterns,
            "relationships_built": relationships,
            "knowledge_gaps": gaps,
            "experience_id": new_experience.id
        }

    def _extract_concepts(self, text: str):
        concepts = []

        definition_patterns = [
            r"(\w+) is (?:a|an) (\w+(?:\s+\w+)*)",
            r"(\w+) means (.*?)",
            r"the (?:term|word) (\w+) refers to (.*?)"
        ]

        for pattern in definition_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                concept_name = match.group(1)
                concept_definition = match.group(2)

                concepts.append({
                    "concept": concept_name,
                    "definition": concept_definition,
                    "confidence": 0.8,
                    "source": "definition_pattern"
                })

        words = re.findall(r"\b\w+\b", text.lower())
        unique_words = set(words)

        common_words = {
            "the", "a", "an", "is", "are", "and", "or", "but", "to", "in", "on", "at"
        }

        for word in unique_words:

            if word not in common_words and len(word) > 3:
                concepts.append({
                    "concept": word,
                    "definition": None,
                    "confidence": 0.3,
                    "source": "frequency_analysis"
                })

        return concepts

    def _learn_from_patterns(self, text: str):
        patterns = []

        qa_patterns = re.findall(r"(\?.*?)(\.|\!\?)", text)

        for question, _ in qa_patterns:
            patterns.append({
                "type": "question_answer",
                "pattern": question.strip(),
                "context": "conversation"
            })

        causality_patterns = re.findall(r"(\w+) (?:causes|leads to|results in) (\w+)", text)

        for cause, effect in causality_patterns:
            patterns.append({
                "type": "causality",
                "pattern": f"{cause} -> {effect}",
                "confidence": 0.7
            })

        return patterns

    def _build_relationships(self, concepts: List[Dict]):
        relationships = []

        for i, concept1 in enumerate(concepts):
            for j, concept2 in enumerate(concepts[i+1:], i+1):
                relationships.append({
                    "concept1": concept1["concept"],
                    "concept2": concept2["concept"],
                    "relationship": "related",
                    "strength": 0.5,
                    "type": "co_occurrence"
                })

        return relationships

    def _analyze_knowledge_gaps(self, concepts: List[Dict]):
        gaps = []

        for concept in concepts:
            if concept["confidence"] < 0.5:
                gaps.append({
                    "concept": concept["concept"],
                    "gap_type": "low_confidence",
                    "priority": "medium"
                })
            elif concept["definition"] in None:
                gaps.append({
                    "concept": concept["concept"],
                    "gap_type": "missing_definition",
                    "priority": "high"
                })
        
        return gaps

    def update_concept_network(self, db: Session, concepts: List[Dict]):
        for concept_data in concepts:
            concept_name = concept_data["concept"]

            existing_concept = db.query(Concept_Network).filter(
                Concept_Network.concept_name == concept_name
            ).first()

            if existing_concept:
                existing_concept.usage_frequency += 1
                existing_concept.last_used = datetime.utcnow()

                if concept_data["definition"] and not existing_concept.concept_definition:
                    existing_concept.concept_definition = concept_data["definition"]
                    existing_concept.confidence = concept_data["confidence"]

            else:
                new_concept = Concept_Network(
                    concept_name = concept_name,
                    concept_definition = concept_data.get("definition"),
                    confidence = concept_data["confidence"],
                    learned_from = [concept_data["source"]]
                )

                add_db(db, new_concept)
