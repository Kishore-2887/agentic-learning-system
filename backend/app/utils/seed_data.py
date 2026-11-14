import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import ContentRequest, GeneratedContent, EvaluationReport, RevisionHistory
from app.utils.markdown_export import content_to_markdown

logger = logging.getLogger(__name__)


def seed_initial_demo_data(db: Session):
    """
    Populates sample initial educational content, evaluations, and revisions
    if database is empty, showcasing the self-evaluation system immediately.
    """
    if db.query(GeneratedContent).count() > 0:
        return

    logger.info("Seeding initial educational sample modules...")

    # Sample 1: Quantum Superposition (Approved after 1 revision)
    req1 = ContentRequest(
        topic="Quantum Computing: Principles of Superposition and Qubits",
        target_audience="Computer Science Undergraduates",
        education_level="University",
        learning_objectives=[
            "Distinguish classical bits from quantum qubits",
            "Understand linear superposition state vectors",
            "Explain quantum measurement and state collapse"
        ],
        content_type="lesson",
        quality_threshold=80.0,
        max_retries=3,
        status="completed",
        created_at=datetime.utcnow() - timedelta(hours=3)
    )
    db.add(req1)
    db.flush()

    raw_json1 = {
        "title": "Quantum Computing: Principles of Superposition and Qubits",
        "topic": "Quantum Computing Superposition",
        "target_audience": "Computer Science Undergraduates",
        "education_level": "University",
        "summary": "An introduction to quantum computational states, mathematical formalisms of qubits, and the observable implications of superposition.",
        "key_concepts": ["Qubit", "Superposition", "Bloch Sphere", "Hadamard Gate", "Wavefunction Collapse"],
        "sections": [
            {
                "title": "1. From Classical Bits to Quantum Qubits",
                "explanation": "Classical computing operates strictly on binary digits (bits) restricted to discrete states |0> or |1>. In contrast, a quantum bit (qubit) exists in a continuous linear combination of orthogonal basis states.",
                "examples": [
                    "Classical example: A standard CMOS transistor holding low voltage (0V) or high voltage (5V).",
                    "Quantum example: An electron spin in a superposition of spin-up and spin-down."
                ],
                "callout_note": "A qubit does not represent an unknown classical bit; it is physically indeterminate until measured.",
                "key_terms": ["Orthogonal basis", "State vector", "Qubit"]
            },
            {
                "title": "2. Mathematical Formulation: State Vectors and the Bloch Sphere",
                "explanation": "Any pure qubit state |psi> can be represented as |psi> = alpha|0> + beta|1>, where alpha and beta are complex probability amplitudes satisfying |alpha|^2 + |beta|^2 = 1. Geometrically, this state maps to coordinates on the unit Bloch sphere.",
                "examples": [
                    "Equal superposition: (|0> + |1>)/sqrt(2) created by applying a Hadamard transform to |0>.",
                    "Phase state: (|0> + i|1>)/sqrt(2) introducing a relative phase angle."
                ],
                "callout_note": "Relative phase is critical: quantum algorithms exploit phase interference to amplify correct solutions.",
                "key_terms": ["Bloch Sphere", "Probability Amplitude", "Hadamard Transform"]
            },
            {
                "title": "3. Quantum Measurement and Wavefunction Collapse",
                "explanation": "Measurement fundamentally alters a quantum state according to the Born Rule. Measuring |psi> yields outcome 0 with probability |alpha|^2 and 1 with probability |beta|^2. Post-measurement, the state instantaneously projects into the measured eigenstate.",
                "examples": [
                    "Measuring 1,000 identically prepared qubits in (|0> + |1>)/sqrt(2) yields approximately 500 zeros and 500 ones."
                ],
                "callout_note": "Measurement is irreversible in standard projective quantum mechanics.",
                "key_terms": ["Born Rule", "Projective Measurement", "State Collapse"]
            }
        ],
        "practice_questions": [
            {
                "question": "What constraint must the probability amplitudes alpha and beta satisfy for a normalized qubit state |psi> = alpha|0> + beta|1>?",
                "options": ["A) alpha + beta = 1", "B) |alpha|^2 + |beta|^2 = 1", "C) alpha * beta = 0", "D) |alpha| = |beta|"],
                "answer": "B",
                "explanation": "The sum of the squared magnitudes of the probability amplitudes must equal 1 by conservation of probability."
            },
            {
                "question": "Applying a Hadamard gate to the ground state |0> produces which state?",
                "options": ["A) |1>", "B) (|0> + |1>)/sqrt(2)", "C) (|0> - |1>)/sqrt(2)", "D) 0"],
                "answer": "B",
                "explanation": "The Hadamard gate maps the computational basis states into balanced superposition states."
            }
        ],
        "key_takeaways": [
            "Superposition allows simultaneous exploration of exponentially large state spaces.",
            "Measurement irreversibly projects a superposition into a single classical outcome.",
            "Quantum algorithms rely on constructive and destructive phase interference."
        ],
        "references_and_further_reading": [
            "Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information. Cambridge University Press.",
            "Preskill, J. (2021). Quantum Computing in the NISQ era and beyond. Quantum, 2, 79."
        ]
    }

    md1 = content_to_markdown(raw_json1)
    content1 = GeneratedContent(
        request_id=req1.id,
        version=2,
        title=raw_json1["title"],
        raw_json=raw_json1,
        markdown_text=md1,
        word_count=len(md1.split()),
        is_published=True,
        status="approved",
        created_at=datetime.utcnow() - timedelta(hours=3)
    )
    db.add(content1)
    db.flush()

    # Initial evaluation (Failed - 73.5)
    eval1_1 = EvaluationReport(
        request_id=req1.id,
        content_id=content1.id,
        iteration=1,
        factual_accuracy=78.0,
        relevance=85.0,
        completeness=68.0,
        clarity_readability=72.0,
        educational_effectiveness=70.0,
        structure_organization=75.0,
        overall_score=75.1,
        passed=False,
        identified_errors=[
            {
                "section": "2. Mathematical Formulation",
                "severity": "moderate",
                "description": "Needs explicit normalization condition and geometric explanation of the Bloch sphere.",
                "unsupported_claim": False
            }
        ],
        missing_concepts=["Born Rule definition", "Hadamard gate matrix representation"],
        improvement_recommendations=[
            "Add concrete mathematical definition of probability conservation.",
            "Include practice questions testing amplitude calculations."
        ],
        unsupported_claims=["Superposition guarantees infinite compute speed without qualification."],
        created_at=datetime.utcnow() - timedelta(hours=3, minutes=10)
    )
    db.add(eval1_1)

    # Revision 1
    rev1 = RevisionHistory(
        request_id=req1.id,
        iteration=1,
        changes_summary="Added formal normalization constraints, Bloch sphere geometric explanation, and Born Rule calculation details.",
        previous_score=75.1,
        new_score=91.4,
        modified_sections=["2. Mathematical Formulation", "3. Quantum Measurement"],
        created_at=datetime.utcnow() - timedelta(hours=3, minutes=5)
    )
    db.add(rev1)

    # Second evaluation (Passed - 91.4)
    eval1_2 = EvaluationReport(
        request_id=req1.id,
        content_id=content1.id,
        iteration=2,
        factual_accuracy=94.0,
        relevance=95.0,
        completeness=90.0,
        clarity_readability=89.0,
        educational_effectiveness=88.0,
        structure_organization=92.0,
        overall_score=91.8,
        passed=True,
        identified_errors=[],
        missing_concepts=[],
        improvement_recommendations=["Meets all pedagogical and factual criteria."],
        unsupported_claims=[],
        created_at=datetime.utcnow() - timedelta(hours=3)
    )
    db.add(eval1_2)

    db.commit()
    logger.info("Sample educational modules seeded successfully.")

