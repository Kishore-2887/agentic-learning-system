from abc import ABC, abstractmethod
from app.schemas import (
    ContentPlan,
    EducationalContentSchema,
    EvaluationResult,
    ImprovementResult,
    FinalValidationResult
)


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_plan(
        self,
        topic: str,
        target_audience: str,
        education_level: str,
        learning_objectives: list,
        content_type: str
    ) -> ContentPlan:
        pass

    @abstractmethod
    async def generate_content(
        self,
        plan: ContentPlan
    ) -> EducationalContentSchema:
        pass

    @abstractmethod
    async def evaluate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan,
        quality_threshold: float
    ) -> EvaluationResult:
        pass

    @abstractmethod
    async def improve_content(
        self,
        content: EducationalContentSchema,
        evaluation: EvaluationResult,
        iteration: int
    ) -> ImprovementResult:
        pass

    @abstractmethod
    async def validate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan
    ) -> FinalValidationResult:
        pass

