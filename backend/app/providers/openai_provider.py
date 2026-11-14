import json
import logging
from typing import List, Dict, Any, Optional
from app.providers.base import BaseLLMProvider
from app.config import settings
from app.schemas import (
    ContentPlan,
    EducationalContentSchema,
    EvaluationResult,
    ImprovementResult,
    FinalValidationResult
)
from app.agents.prompts import (
    PLANNER_SYSTEM_PROMPT,
    GENERATOR_SYSTEM_PROMPT,
    EVALUATOR_SYSTEM_PROMPT,
    IMPROVER_SYSTEM_PROMPT,
    VALIDATOR_SYSTEM_PROMPT
)

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        if not self.api_key:
            raise ValueError("OpenAI API key is not configured.")

        from langchain_openai import ChatOpenAI
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0.3
        )

    async def generate_plan(
        self,
        topic: str,
        target_audience: str,
        education_level: str,
        learning_objectives: list,
        content_type: str
    ) -> ContentPlan:
        structured_llm = self.llm.with_structured_output(ContentPlan)
        prompt = (
            f"{PLANNER_SYSTEM_PROMPT}\n\n"
            f"Topic: {topic}\n"
            f"Target Audience: {target_audience}\n"
            f"Education Level: {education_level}\n"
            f"Learning Objectives: {learning_objectives}\n"
            f"Content Type: {content_type}"
        )
        return await structured_llm.ainvoke(prompt)

    async def generate_content(
        self,
        plan: ContentPlan
    ) -> EducationalContentSchema:
        structured_llm = self.llm.with_structured_output(EducationalContentSchema)
        prompt = (
            f"{GENERATOR_SYSTEM_PROMPT}\n\n"
            f"Approved Plan JSON:\n{plan.model_dump_json(indent=2)}"
        )
        return await structured_llm.ainvoke(prompt)

    async def evaluate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan,
        quality_threshold: float
    ) -> EvaluationResult:
        structured_llm = self.llm.with_structured_output(EvaluationResult)
        prompt = (
            f"{EVALUATOR_SYSTEM_PROMPT.format(quality_threshold=quality_threshold)}\n\n"
            f"Original Plan Requirements:\n{plan.model_dump_json(indent=2)}\n\n"
            f"Generated Educational Content:\n{content.model_dump_json(indent=2)}"
        )
        result: EvaluationResult = await structured_llm.ainvoke(prompt)
        # Recalculate deterministic weighted score to guarantee compliance
        calc_score = round(
            (result.factual_accuracy * 0.25) +
            (result.relevance * 0.20) +
            (result.completeness * 0.20) +
            (result.clarity_readability * 0.15) +
            (result.educational_effectiveness * 0.10) +
            (result.structure_organization * 0.10),
            1
        )
        result.overall_score = calc_score
        result.passed = calc_score >= quality_threshold
        return result

    async def improve_content(
        self,
        content: EducationalContentSchema,
        evaluation: EvaluationResult,
        iteration: int
    ) -> ImprovementResult:
        structured_llm = self.llm.with_structured_output(ImprovementResult)
        prompt = (
            f"{IMPROVER_SYSTEM_PROMPT}\n\n"
            f"Iteration Number: {iteration}\n\n"
            f"Current Content JSON:\n{content.model_dump_json(indent=2)}\n\n"
            f"Evaluation Critique & Identified Issues:\n{evaluation.model_dump_json(indent=2)}"
        )
        return await structured_llm.ainvoke(prompt)

    async def validate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan
    ) -> FinalValidationResult:
        structured_llm = self.llm.with_structured_output(FinalValidationResult)
        prompt = (
            f"{VALIDATOR_SYSTEM_PROMPT}\n\n"
            f"Original Plan Blueprint:\n{plan.model_dump_json(indent=2)}\n\n"
            f"Final Content for Publication:\n{content.model_dump_json(indent=2)}"
        )
        return await structured_llm.ainvoke(prompt)

