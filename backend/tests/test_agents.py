import pytest
from app.providers.mock_provider import MockLLMProvider
from app.schemas import ContentPlan, EducationalContentSchema, EvaluationResult


@pytest.mark.asyncio
async def test_planner_agent():
    provider = MockLLMProvider()
    plan = await provider.generate_plan(
        topic="Machine Learning Gradient Descent",
        target_audience="Data Science Beginners",
        education_level="College",
        learning_objectives=["Understand cost functions", "Compute gradients"],
        content_type="lesson"
    )

    assert plan.topic == "Machine Learning Gradient Descent"
    assert len(plan.outline) >= 3
    assert len(plan.evaluation_criteria) >= 2


@pytest.mark.asyncio
async def test_generator_agent():
    provider = MockLLMProvider()
    plan = await provider.generate_plan(
        topic="Machine Learning Gradient Descent",
        target_audience="Data Science Beginners",
        education_level="College",
        learning_objectives=["Understand cost functions"],
        content_type="lesson"
    )

    content = await provider.generate_content(plan)
    assert content.title is not None
    assert len(content.sections) == len(plan.outline)
    assert len(content.practice_questions) >= 2


@pytest.mark.asyncio
async def test_evaluator_scoring_weights():
    provider = MockLLMProvider()
    plan = await provider.generate_plan(
        topic="Python Concurrency",
        target_audience="Intermediate Developers",
        education_level="Professional",
        learning_objectives=["Asyncio vs Threading"],
        content_type="lesson"
    )
    content = await provider.generate_content(plan)

    evaluation = await provider.evaluate_content(content, plan, quality_threshold=80.0)

    # Verify calculation:
    # 25% Factual, 20% Relevance, 20% Completeness, 15% Clarity, 10% Educational, 10% Structure
    expected = round(
        (evaluation.factual_accuracy * 0.25) +
        (evaluation.relevance * 0.20) +
        (evaluation.completeness * 0.20) +
        (evaluation.clarity_readability * 0.15) +
        (evaluation.educational_effectiveness * 0.10) +
        (evaluation.structure_organization * 0.10),
        1
    )
    assert abs(evaluation.overall_score - expected) < 0.1
    assert evaluation.passed == (evaluation.overall_score >= 80.0)


@pytest.mark.asyncio
async def test_improver_agent():
    provider = MockLLMProvider()
    plan = await provider.generate_plan(
        topic="Database Indexing",
        target_audience="Backend Developers",
        education_level="Professional",
        learning_objectives=["B-Trees vs Hash Indexes"],
        content_type="lesson"
    )
    content = await provider.generate_content(plan)
    evaluation = await provider.evaluate_content(content, plan, quality_threshold=80.0)

    # First iteration should have issues to trigger improver
    assert not evaluation.passed

    improvement = await provider.improve_content(content, evaluation, iteration=1)
    assert len(improvement.modified_sections) > 0
    assert len(improvement.improvements_applied) > 0

    # Re-evaluating improved content should score higher
    re_evaluation = await provider.evaluate_content(improvement.revised_content, plan, quality_threshold=80.0)
    assert re_evaluation.overall_score > evaluation.overall_score
    assert re_evaluation.passed is True

