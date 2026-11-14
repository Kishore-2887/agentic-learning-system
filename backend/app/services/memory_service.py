import json
import os
import logging
from typing import List

logger = logging.getLogger(__name__)

MEMORY_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_memory.json")

DEFAULT_LEARNED_RULES = [
    "Target Audience Rule: For 12th-grade Indian students with non-English medium backgrounds, always explain concepts using everyday analogies like an 'Open-Book vs Closed-Book Exam'.",
    "Jargon Rule: Never introduce technical acronyms (LLM, RAG, Embeddings) without immediate plain-English translation (e.g. 'LLM is like a very well-read student; RAG is giving that student the open textbook').",
    "Grounding Rule: Explicitly contrast RAG with fine-tuning. Clarify that RAG does NOT retrain the model weights; it simply retrieves fresh reference notes at query time.",
    "Structure Rule: Always clearly isolate the 3 phases: 1) Retrieve (Search relevant text), 2) Augment (Attach found text to prompt), and 3) Generate (Produce grounded response).",
    "Engagement Rule: Provide interactive check-your-understanding questions with reassuring explanations to build learner confidence in AI careers."
]


class MemoryService:
    @staticmethod
    def get_learned_rules() -> List[str]:
        if not os.path.exists(MEMORY_FILE_PATH):
            MemoryService.save_rules(DEFAULT_LEARNED_RULES)
            return DEFAULT_LEARNED_RULES

        try:
            with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("rules", DEFAULT_LEARNED_RULES)
        except Exception as e:
            logger.warning(f"Failed to read agent memory ({e}). Using defaults.")
            return DEFAULT_LEARNED_RULES

    @staticmethod
    def save_rules(rules: List[str]):
        try:
            with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump({"rules": rules}, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to write agent memory: {e}")

    @staticmethod
    def record_rejection_lesson(critique: str, failed_checkpoints: List[str]):
        """
        Self-evolving feedback loop:
        Extracts actionable rules from evaluator rejections so future generations don't repeat mistakes.
        """
        rules = MemoryService.get_learned_rules()
        new_rule = f"Learned from Rejection [{', '.join(failed_checkpoints)}]: {critique[:120]}..."
        if new_rule not in rules:
            rules.append(new_rule)
            MemoryService.save_rules(rules)
            logger.info(f"Agent Memory self-evolved with new learned heuristic: {new_rule}")


memory_service = MemoryService()

