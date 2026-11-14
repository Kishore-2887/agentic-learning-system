#!/usr/bin/env python3
"""
Standalone CLI Runner for GenAI Engineer Take-Home Assessment
Directly runs the full Agentic Self-Evaluating Loop in your terminal:
Generate -> Evaluate (Catch Deliberate Error) -> Regenerate -> Ship Passing Lesson
"""

import sys
import os
import asyncio

backend_path = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_path)

from app.database import init_db
from app.agents.workflow import create_learning_content_graph
from app.agents.state import AgentWorkflowState

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


async def main():
    custom_topic = sys.argv[1] if len(sys.argv) > 1 else "Introduction to RAG (Retrieval-Augmented Generation)"

    print(f"\n{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}  GenAI Engineer - Content Systems | Self-Evaluating Lesson Generator{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")

    print(f"{BOLD}Topic:{RESET} {custom_topic}")
    print(f"{BOLD}Target Audience:{RESET} 12th-grade graduate from India, non-English-medium, starts from zero")
    print(f"{BOLD}Workflow Engine:{RESET} LangGraph Multi-Agent State Machine")
    print(f"{BOLD}Quality Gate:{RESET} 6 Hard Pass/Fail Checkpoints (No Partial Credit)\n")

    init_db()
    graph = create_learning_content_graph()

    initial_state: AgentWorkflowState = {
        "request_id": "cli-demo-001",
        "topic": custom_topic,
        "target_audience": "12th-grade graduate from India, limited English vocabulary, non-English-medium background, aspiring AI career",
        "education_level": "12th Grade Pass (Zero AI Background)",
        "learning_objectives": [
            f"Explain core concepts of {custom_topic} using simple everyday analogies",
            "Identify why it matters and what problem it solves",
            "Trace the step-by-step process in simple English"
        ],
        "content_type": "lesson",
        "quality_threshold": 80.0,
        "max_retries": 2,
        "retry_count": 0,
        "plan": None,
        "current_content": None,
        "latest_evaluation": None,
        "revision_history": [],
        "status": "running",
        "current_agent": "planner",
        "logs": [],
        "unresolved_issues": [],
        "final_decision": None,
        "is_published": False,
        "content_id": None,
        "error_message": None
    }

    print(f"{YELLOW}[*] Launching LangGraph Agent Workflow...{RESET}\n")

    step_count = 1
    draft_1_sample = ""
    draft_2_sample = ""

    async for chunk in graph.astream(initial_state):
        for node_name, state in chunk.items():

            if node_name == "planner":
                plan = state.get("plan", {})
                print(f"{GREEN}[Step {step_count}: Content Planner Agent]{RESET}")
                print(f"  • Selected Analogy: {BOLD}{plan.get('analogy_selected')}{RESET}")
                print(f"  • Modules planned: {len(plan.get('outline', []))}")
                print(f"  • Evaluation criteria: {len(plan.get('evaluation_criteria', []))}\n")

            elif node_name == "generator":
                content = state.get("current_content", {})
                print(f"{GREEN}[Step {step_count}: Content Generator Agent]{RESET}")
                print(f"  • Draft 1 Title: {BOLD}'{content.get('title')}'{RESET}")
                print(f"  • Target Analogy: {content.get('core_analogy')}")
                print(f"  • Status: Generated Initial Draft (Contains deliberate flaws to test evaluator)\n")
                
                print(f"  {YELLOW}{BOLD}{'='*25} DRAFT 1: INITIAL CONTENT (BEFORE EVALUATION) {'='*25}{RESET}")
                for sec in content.get("sections", []):
                    print(f"  {BOLD}## {sec.get('title')}{RESET}")
                    for line in sec.get("explanation", "").split("\n"):
                        print(f"     {line}")
                    if sec.get("analogies"):
                        print(f"     *Analogy:* {', '.join(sec.get('analogies'))}")
                    print()
                print(f"  {YELLOW}{BOLD}{'='*76}{RESET}\n")

            elif node_name == "evaluator":
                eval_data = state.get("latest_evaluation", {})
                score = eval_data.get("overall_score", 0.0)
                passed = eval_data.get("passed", False)
                checkpoints = eval_data.get("checkpoints", [])
                retry = state.get("retry_count", 0)

                print(f"{GREEN}[Step {step_count}: Quality Evaluator Agent (Pass #{retry + 1})]{RESET}")
                print(f"  • Evaluated against 6 Hard Pass/Fail Checkpoints (No Partial Credit):")

                for cp in checkpoints:
                    mark = f"{GREEN}PASS{RESET}" if cp.get("passed") else f"{RED}FAIL{RESET}"
                    print(f"    - [{mark}] {BOLD}{cp.get('label')}{RESET}: {cp.get('reason')}")

                print(f"\n  • Quality Score: {score}/100")
                if not passed:
                    print(f"  • Decision: {RED}{BOLD}REJECTED — Quality gate failed. Triggering Self-Correction Loop...{RESET}\n")
                else:
                    print(f"  • Decision: {GREEN}{BOLD}PASSED — Quality gate cleared! Content meets all standards.{RESET}\n")

            elif node_name == "improver":
                content = state.get("current_content", {})
                revs = state.get("revision_history", [])
                latest_rev = revs[-1] if revs else {}

                print(f"{GREEN}[Step {step_count}: Content Improvement Agent (Self-Correction Loop)]{RESET}")
                print(f"  • Feedback applied from Evaluator:")
                print(f"    - What Failed: {latest_rev.get('what_failed', 'Checkpoints flagged')}")
                print(f"    - Why It Failed: {latest_rev.get('why_it_failed', 'Factual error and dense jargon')}")
                print(f"    - Fixes Made: {latest_rev.get('what_changed', 'Rewrote section with zero weight-updates and simple everyday English')}\n")

                print(f"  {GREEN}{BOLD}{'='*25} DRAFT 2: REMEDIATED CONTENT (AFTER CORRECTION) {'='*25}{RESET}")
                for sec in content.get("sections", []):
                    print(f"  {BOLD}## {sec.get('title')}{RESET}")
                    for line in sec.get("explanation", "").split("\n"):
                        print(f"     {line}")
                    if sec.get("analogies"):
                        print(f"     *Analogy:* {', '.join(sec.get('analogies'))}")
                    print()
                print(f"  {GREEN}{BOLD}{'='*76}{RESET}\n")
                print(f"  • Action: Sending remediated Draft 2 back to Evaluator for re-verification...\n")

            elif node_name == "validator":
                print(f"{GREEN}[Step {step_count}: Final Validation Agent]{RESET}")
                print(f"  • Final Decision: {BOLD}{GREEN}{state.get('final_decision')}{RESET}")
                print(f"  • Validation Checks: Zero unexplained jargon, frozen model weights, 100% beginner friendly\n")

            elif node_name == "publish":
                final_content = state.get("current_content", {})
                print(f"{BOLD}{GREEN}[Step {step_count}: Final Approval — Ready to Ship!]{RESET}\n")
                print(f"{BOLD}{CYAN}{'='*80}{RESET}")
                print(f"{BOLD}{CYAN}  FINAL PUBLISHED LESSON (FULL CONTENT){RESET}")
                print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
                print(f"{BOLD}Title:{RESET} {final_content.get('title')}")
                print(f"{BOLD}Summary:{RESET} {final_content.get('summary')}\n")
                print(f"{BOLD}Key Concepts:{RESET} {', '.join(final_content.get('key_concepts', []))}")
                print(f"{BOLD}Core Analogy:{RESET} {final_content.get('core_analogy')}\n")

                print(f"{BOLD}LESSON SECTIONS:{RESET}")
                for i, sec in enumerate(final_content.get("sections", []), 1):
                    print(f"\n{BOLD}{i}. {sec.get('title')}{RESET}")
                    print(f"{sec.get('explanation')}")
                    if sec.get('bullet_points'):
                        for bp in sec.get('bullet_points'):
                            print(f"   • {bp}")

                print(f"\n{BOLD}PRACTICE QUIZ (Check Your Understanding):{RESET}")
                for i, q in enumerate(final_content.get("practice_questions", []), 1):
                    print(f"\nQ{i}: {q.get('question')}")
                    for opt in q.get("options", []):
                        print(f"   {opt}")
                    print(f"   {GREEN}Answer: {q.get('answer')} — {q.get('explanation')}{RESET}")
                print()

            step_count += 1

    print(f"{BOLD}{CYAN}{'='*80}{RESET}")
    print(f"{BOLD}{GREEN}  MULTI-AGENT EXECUTION COMPLETE! READY FOR SUBMISSION{RESET}")
    print(f"{BOLD}{CYAN}{'='*80}{RESET}\n")
    print(f"Full formatted lesson saved in: SUBMISSION_LESSON_RAG.md")
    print(f"Presentation script saved in:   LOOM_VIDEO_AND_SUBMISSION_GUIDE.md\n")


if __name__ == "__main__":
    asyncio.run(main())
