import json
import logging
import re
from typing import Optional
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


def clean_json_response(text: str) -> str:
    """Strip markdown code blocks if present."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text


class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model or settings.GEMINI_MODEL
        if not self.api_key:
            raise ValueError("Gemini API key is not configured.")

        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    async def _generate_structured(self, prompt: str, schema_class):
        full_prompt = (
            f"{prompt}\n\n"
            f"You MUST return ONLY valid JSON matching this schema description:\n"
            f"{json.dumps(schema_class.model_json_schema(), indent=2)}\n"
            f"Do not include any conversational preamble or postscript."
        )
        response = await self.model.generate_content_async(full_prompt)
        cleaned = clean_json_response(response.text)
        data = json.loads(cleaned)
        return schema_class.model_validate(data)

    async def generate_plan(
        self,
        topic: str,
        target_audience: str,
        education_level: str,
        learning_objectives: list,
        content_type: str
    ) -> ContentPlan:
        prompt = (
            f"{PLANNER_SYSTEM_PROMPT}\n\n"
            f"Topic: {topic}\n"
            f"Target Audience: {target_audience}\n"
            f"Education Level: {education_level}\n"
            f"Learning Objectives: {learning_objectives}\n"
            f"Content Type: {content_type}"
        )
        return await self._generate_structured(prompt, ContentPlan)

    async def generate_content(
        self,
        plan: ContentPlan
    ) -> EducationalContentSchema:
        prompt = (
            f"{GENERATOR_SYSTEM_PROMPT}\n\n"
            f"Approved Plan:\n{plan.model_dump_json(indent=2)}"
        )
        return await self._generate_structured(prompt, EducationalContentSchema)

    async def evaluate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan,
        quality_threshold: float
    ) -> EvaluationResult:
        prompt = (
            f"{EVALUATOR_SYSTEM_PROMPT.format(quality_threshold=quality_threshold)}\n\n"
            f"Original Plan:\n{plan.model_dump_json(indent=2)}\n\n"
            f"Content to Evaluate:\n{content.model_dump_json(indent=2)}"
        )
        result: EvaluationResult = await self._generate_structured(prompt, EvaluationResult)
        # Recalculate deterministic weighted score
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
        prompt = (
            f"{IMPROVER_SYSTEM_PROMPT}\n\n"
            f"Iteration Number: {iteration}\n\n"
            f"Current Content:\n{content.model_dump_json(indent=2)}\n\n"
            f"Evaluation Critique:\n{evaluation.model_dump_json(indent=2)}"
        )
        return await self._generate_structured(prompt, ImprovementResult)

    async def validate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan
    ) -> FinalValidationResult:
        prompt = (
            f"{VALIDATOR_SYSTEM_PROMPT}\n\n"
            f"Original Plan:\n{plan.model_dump_json(indent=2)}\n\n"
            f"Final Content:\n{content.model_dump_json(indent=2)}"
        )
        return await self._generate_structured(prompt, FinalValidationResult)

