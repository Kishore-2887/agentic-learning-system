import asyncio
from typing import List, Dict, Any
from app.providers.base import BaseLLMProvider
from app.schemas import (
    ContentPlan,
    PlanSection,
    EducationalContentSchema,
    ContentSection,
    PracticeQuestion,
    EvaluationResult,
    IdentifiedError,
    ImprovementResult,
    FinalValidationResult,
    RubricCheckpoint
)
from app.services.memory_service import memory_service


class MockLLMProvider(BaseLLMProvider):
    """
    Intelligent simulated LLM provider:
    - Generates dynamic, beginner-friendly content for ANY topic entered by the user.
    - Demonstrates: Evaluator catching deliberate errors (Pass 1) -> Remediation & Analogy Injection -> Approved Shipping (Pass 2).
    """

    async def generate_plan(
        self,
        topic: str,
        target_audience: str,
        education_level: str,
        learning_objectives: list,
        content_type: str
    ) -> ContentPlan:
        await asyncio.sleep(0.8)

        is_rag = "rag" in topic.lower()
        is_api = "api" in topic.lower()

        if is_rag:
            analogy = "Open-Book Exam vs Closed-Book Exam"
            objectives = learning_objectives if learning_objectives else [
                "Understand why AI models make mistakes or have outdated knowledge",
                "Explain RAG using the simple 'Open-Book vs Closed-Book Exam' analogy",
                "Break down the 3 steps: Retrieve (Search), Augment (Attach), Generate (Answer)",
                "Identify why RAG is a foundational skill for an entry-level AI career"
            ]
            outline = [
                PlanSection(
                    title="1. The Big AI Problem: Why Does ChatGPT Sometimes Make Things Up?",
                    subtopics=["What is Hallucination?", "The Cutoff Date Problem", "Closed-Book Exam Analogy"],
                    target_learning_outcome="Understand the limitations of regular AI without external notes."
                ),
                PlanSection(
                    title="2. What is RAG? The Open-Book Exam Secret",
                    subtopics=["RAG Meaning Explained Simply", "How it Differs from Retraining/Fine-tuning", "The Library & Student Analogy"],
                    target_learning_outcome="Define RAG intuitively without any confusing mathematical jargon."
                ),
                PlanSection(
                    title="3. How RAG Works: Step-by-Step (Retrieve, Augment, Generate)",
                    subtopics=["Step 1: Retrieve (Finding the Page)", "Step 2: Augment (Giving Notes to the AI)", "Step 3: Generate (Writing the Grounded Answer)"],
                    target_learning_outcome="Trace the lifecycle of a question moving through a RAG pipeline."
                ),
                PlanSection(
                    title="4. Why RAG Matters for Your Future Career in AI",
                    subtopics=["Every Company Uses RAG", "No Need for Million-Dollar Supercomputers", "Summary & Encouragement"],
                    target_learning_outcome="Connect technical RAG concepts directly to practical career opportunities."
                )
            ]
        elif is_api:
            analogy = "The Restaurant Waiter Analogy"
            objectives = learning_objectives if learning_objectives else [
                "Understand what an API is in simple, everyday language",
                "Explain APIs using the Restaurant Waiter analogy (Customer, Waiter, Kitchen)",
                "Understand how mobile apps (like Zomato and UPI) use APIs to talk to servers",
                "Why APIs are the backbone of all modern software engineering"
            ]
            outline = [
                PlanSection(
                    title="1. What is an API? The Restaurant Waiter Analogy",
                    subtopics=["Customer (You)", "Waiter (API)", "Kitchen (Server/Database)"],
                    target_learning_outcome="Understand API definition without reading complex technical manuals."
                ),
                PlanSection(
                    title="2. Real-World Examples: How Your Phone Uses APIs Every Day",
                    subtopics=["Google Maps in Zomato/Uber", "UPI Payments in PhonePe/GPay", "Weather Apps"],
                    target_learning_outcome="See how different apps talk to each other through APIs."
                ),
                PlanSection(
                    title="3. Request and Response: How the Conversation Works",
                    subtopics=["Making a Request (Ordering Food)", "Sending Response (Serving the Dish)", "Data in JSON format"],
                    target_learning_outcome="Understand request and response cycles in plain English."
                ),
                PlanSection(
                    title="4. Why Learning APIs is Your Gateway to a Tech Career",
                    subtopics=["Every Developer Uses APIs", "Frontend and Backend Bridge", "Summary & Encouragement"],
                    target_learning_outcome="Connect API knowledge to beginner tech jobs."
                )
            ]
        else:
            analogy = f"Foundational Everyday Example for {topic}"
            objectives = learning_objectives if learning_objectives else [
                f"Understand core concepts of {topic} from zero",
                f"Explain {topic} using simple everyday analogies",
                f"Examine real-world applications and beginner career paths"
            ]
            outline = [
                PlanSection(
                    title=f"1. Introduction: What is {topic}?",
                    subtopics=["Basic Definition", "Everyday Analogy", "Common Beginner Questions"],
                    target_learning_outcome=f"Build clear mental model of {topic}."
                ),
                PlanSection(
                    title=f"2. How {topic} Works Behind the Scenes",
                    subtopics=["Core Mechanism", "Step-by-Step Breakdown", "Key Invariants"],
                    target_learning_outcome=f"Understand mechanics of {topic} without heavy math."
                ),
                PlanSection(
                    title=f"3. Real-World Applications & Industry Use Cases",
                    subtopics=["Everyday Examples", "Company Case Studies", "Common Pitfalls"],
                    target_learning_outcome=f"See {topic} in actual production practice."
                ),
                PlanSection(
                    title=f"4. Next Steps & Career Value in Modern Tech",
                    subtopics=["Why Companies Value This Skill", "Hands-on Practice", "Summary"],
                    target_learning_outcome="Connect this knowledge to future tech opportunities."
                )
            ]

        criteria = [
            "Accurate & grounded (technically correct concepts)",
            "Beginner-friendly language for 12th-grade Indian student from non-English medium",
            f"Teaches by relatable example ({analogy})",
            "Zero unexplained jargon (every acronym clearly translated)",
            "Covers the 3 key points: What it is, Why it matters, How it works",
            "Coherent teaching flow ending with interactive practice questions"
        ]

        return ContentPlan(
            topic=topic,
            target_audience=target_audience,
            education_level=education_level,
            learning_objectives=objectives,
            difficulty_level="Beginner (Accessible for 12th Grade non-English-medium)",
            outline=outline,
            evaluation_criteria=criteria,
            analogy_selected=analogy
        )

    async def generate_content(
        self,
        plan: ContentPlan
    ) -> EducationalContentSchema:
        await asyncio.sleep(1.0)

        topic = plan.topic
        is_rag = "rag" in topic.lower()
        is_api = "api" in topic.lower()

        if is_rag:
            title = "Introduction to RAG (Retrieval-Augmented Generation)"
            summary = "A beginner-friendly lesson on RAG designed for Indian learners starting from zero. Explains why AI hallucinates, how the Open-Book Exam analogy works, and the 3-step Retrieve-Augment-Generate pipeline."
            core_analogy = "Open-Book Exam vs Closed-Book Exam"
            key_concepts = ["LLM", "Hallucination", "RAG", "Retrieve", "Augment", "Generate"]

            sections = [
                ContentSection(
                    title=plan.outline[0].title,
                    explanation=(
                        "Imagine you are sitting for your 12th board exams. If the teacher says you cannot look at any books, "
                        "you must write whatever you remember from memory. This is called a Closed-Book Exam.\n\n"
                        "Today's AI tools like ChatGPT work just like that student. During training, they read billions of internet pages. "
                        "When you ask a question, they answer purely from memory. But what if you ask about a cricket match that happened "
                        "yesterday, or your school's private exam schedule? The AI does not have that in memory. Sometimes, instead of saying "
                        "'I don't know', it speaks with full confidence and makes up fake facts! In the AI world, we call this a Hallucination."
                    ),
                    examples=[
                        "Real Example: Asking an AI for today's petrol price in Mumbai — without external search, it guesses an old number.",
                        "Analogy: A student answering a question on an exam paper from half-remembered rumors."
                    ],
                    callout_note="Remember: An AI without extra tools is only as smart as what it memorized before its training cutoff date.",
                    key_terms=["LLM (Large Language Model - like ChatGPT)", "Hallucination (AI making up fake facts with confidence)", "Training Cutoff (The date AI stopped learning new data)"]
                ),
                ContentSection(
                    title=plan.outline[1].title,
                    explanation=(
                        "This is where RAG comes in! RAG stands for Retrieval-Augmented Generation.\n\n"
                        "Now, instead of a closed-book exam, imagine the teacher tells you: 'You can bring your textbook into the exam hall.' "
                        "This is an Open-Book Exam. You don't have to memorize thousands of pages. You just need to know how to look up "
                        "the right topic in the index, read the paragraph, and write your answer.\n\n"
                        "[DELIBERATE FLAW INJECTED ON DRAFT 1]: "
                        "Technically, RAG works by constantly retraining the neural network weights of the AI model on your PDF documents every time you query it, "
                        "optimizing high-dimensional manifold cosine similarity embeddings without token-level loss."
                    ),
                    examples=[
                        "Library Analogy: A student looking at the library catalog to find the exact book before answering."
                    ],
                    callout_note="Key takeaway: Open-book exam means the AI is given exact facts before answering.",
                    key_terms=["RAG (Retrieval-Augmented Generation)", "Open-Book Exam"]
                ),
                ContentSection(
                    title=plan.outline[2].title,
                    explanation=(
                        "RAG happens in three simple steps that you can remember by the letters R - A - G:\n\n"
                        "1. R - RETRIEVE (Search the right page): When you ask a question (like 'What is my company's leave policy?'), "
                        "the system first searches through your documents to find the 2 or 3 most relevant paragraphs.\n\n"
                        "2. A - AUGMENT (Give notes to AI): Next, the system takes your question AND attaches those found paragraphs together. "
                        "'Augment' is just a fancy English word that means 'to add or give extra'. We are giving extra notes to the AI.\n\n"
                        "3. G - GENERATE (Write the answer): Finally, the AI reads your question and the notes, and writes a neat, accurate response "
                        "strictly based on those notes."
                    ),
                    examples=[
                        "Customer Care Bot: When you ask about your bus refund on redBus, RAG fetches your exact ticket details and answers correctly."
                    ],
                    callout_note="Formula: Your Question + Found Document Notes = Grounded, Accurate Answer.",
                    key_terms=["Retrieve (Search)", "Augment (Add notes)", "Generate (Write response)"]
                ),
                ContentSection(
                    title=plan.outline[3].title,
                    explanation=(
                        "Why is RAG so important if you want an AI career? Training a big AI model from scratch costs millions of dollars "
                        "and thousands of GPUs. Most Indian startups, hospitals, banks, and IT companies cannot afford that.\n\n"
                        "Instead, 90% of real AI jobs in industry involve building RAG systems! By learning RAG, you can build smart AI assistants "
                        "that answer from medical records, legal PDFs, college notes, or Hindi/Tamil documents — in minutes, without spending crores of rupees. "
                        "You don't need a PhD in advanced mathematics to start. You just need to understand this 3-step pipeline!"
                    ),
                    examples=[
                        "Hospital assistant searching medical reports in 2 seconds.",
                        "College study bot answering questions directly from state board textbooks."
                    ],
                    callout_note="Career Tip: Every company has private documents they want to chat with. RAG is the bridge.",
                    key_terms=["Industry Application", "Practical AI Career", "Zero Model Retraining Cost"]
                )
            ]

            practice_questions = [
                PracticeQuestion(
                    question="What is the best everyday analogy to explain RAG to someone starting from zero?",
                    options=[
                        "A) An Open-Book Exam where the student looks up notes before answering",
                        "B) A Closed-Book Exam where you only answer from memory",
                        "C) Buying a new computer processor",
                        "D) Erasing the AI's memory permanently"
                    ],
                    answer="A",
                    explanation="RAG gives the AI reference notes (textbook) at question time, exactly like an Open-Book Exam."
                ),
                PracticeQuestion(
                    question="What are the three core steps of RAG?",
                    options=[
                        "A) Restart, Announce, Goodbye",
                        "B) Retrieve, Augment, Generate",
                        "C) Retrain, Analyze, Guess",
                        "D) Read, Argue, Google"
                    ],
                    answer="B",
                    explanation="R = Retrieve relevant text, A = Augment prompt with notes, G = Generate grounded answer."
                ),
                PracticeQuestion(
                    question="Why is RAG preferred by companies over retraining large models?",
                    options=[
                        "A) Retraining is cheap and takes 2 seconds",
                        "B) RAG requires zero retraining of weights and provides updated, private answers at low cost",
                        "C) RAG does not work on PDFs",
                        "D) AI cannot read text"
                    ],
                    answer="B",
                    explanation="RAG avoids multimillion-dollar retraining costs while providing grounded, updated answers."
                )
            ]

            takeaways = [
                "Standard AI is like a Closed-Book Exam: it only knows what it memorized in the past.",
                "RAG turns AI into an Open-Book Exam: it searches fresh documents before answering.",
                "The 3-step pipeline is: Retrieve (search) -> Augment (give notes) -> Generate (write answer).",
                "RAG does NOT retrain the AI weights; it operates cleanly at question time.",
                "RAG is the #1 in-demand practical skill for entry-level AI engineers in India."
            ]
        elif is_api:
            title = "What is an API? The Friendly Beginner's Guide"
            summary = "A beginner-friendly introduction to APIs using the famous Restaurant Waiter analogy. Explains how mobile apps, websites, and payments communicate behind the scenes."
            core_analogy = "The Restaurant Waiter (Customer, Waiter, Kitchen)"
            key_concepts = ["API", "Client / Customer", "Server / Kitchen", "Request", "Response", "JSON"]

            sections = [
                ContentSection(
                    title=plan.outline[0].title,
                    explanation=(
                        "Imagine you go to a restaurant to eat biryani. You are the customer sitting at the table. "
                        "The kitchen where the chef cooks the food is in the back.\n\n"
                        "Can you walk straight into the kitchen, open the gas stove, and take the food yourself? No! "
                        "Instead, the restaurant gives you a **Waiter**.\n\n"
                        "- You tell the waiter: 'One chicken biryani, please.' (This is called a **Request**).\n"
                        "- The waiter walks to the kitchen, tells the chef, picks up the cooked dish, and brings it back to your table. (This is called a **Response**).\n\n"
                        "In the software world, an **API** (Application Programming Interface) is exactly like that waiter! "
                        "It connects two different computer programs so they can talk safely without messing with each other's kitchen."
                    ),
                    examples=[
                        "Restaurant Analogy: Customer (Your App) -> Waiter (API) -> Kitchen (Server Database).",
                        "Real App Example: When you book an Uber or Ola, the app asks Google Maps API: 'Show me the road to the railway station.'"
                    ],
                    callout_note="Definition: API stands for Application Programming Interface. It is simply a waiter that carries messages between apps.",
                    key_terms=["API (Messenger/Waiter between apps)", "Client (The person/app asking)", "Server (The computer answering)"]
                ),
                ContentSection(
                    title=plan.outline[1].title,
                    explanation=(
                        "You already use dozens of APIs every single day without realizing it!\n\n"
                        "1. **Food Delivery (Zomato / Swiggy):** Zomato doesn't own satellites in space. When you track your delivery boy on the map, "
                        "Zomato uses the **Google Maps API** to show the map.\n\n"
                        "2. **Online Payments (GPay / PhonePe / Paytm):** When you scan a QR code to pay ₹50 at a tea stall, the app uses a **Bank UPI API** "
                        "to securely ask the bank: 'Deduct ₹50 from my account and send it to the shopkeeper.'\n\n"
                        "[DELIBERATE FLAW INJECTED ON DRAFT 1]: "
                        "Technically, an API works by executing raw kernel assembly instructions across distributed microarchitectures with zero abstraction layers, "
                        "directly reading server RAM registers without authentication protocols."
                    ),
                    examples=[
                        "Weather Widget on Phone: The phone doesn't have a thermometer inside; it calls a Weather API to get Mumbai's temperature."
                    ],
                    callout_note="Remember: APIs let companies reuse existing services instead of rebuilding everything from zero.",
                    key_terms=["Google Maps API", "UPI Payment API", "Weather API"]
                ),
                ContentSection(
                    title=plan.outline[2].title,
                    explanation=(
                        "Every API interaction has two simple parts:\n\n"
                        "1. **REQUEST (The Question):** Your app sends a message to the server: 'Hey, show me the top 10 movies today.'\n"
                        "2. **RESPONSE (The Answer):** The server sends back the data, usually in a clean text format called **JSON** "
                        "(which looks like a simple grocery list: name: 'Movie Name', rating: 9.2).\n\n"
                        "Just like a waiter needs you to order from the menu (you can't order pizza at an ice cream shop), "
                        "an API has clear rules on what requests it accepts."
                    ),
                    examples=[
                        "Booking a train ticket on IRCTC: Request has Date & Destination; Response has Train List & Seat Availability."
                    ],
                    callout_note="Formula: Request (Ordering food) -> Response (Getting your dish).",
                    key_terms=["Request (Message sent)", "Response (Message received)", "JSON (Clean text data format)"]
                ),
                ContentSection(
                    title=plan.outline[3].title,
                    explanation=(
                        "Why does learning APIs matter for your tech career in India?\n\n"
                        "Every modern job in software — whether you build mobile apps, websites, AI chatbots, or cloud software — "
                        "requires connecting to APIs. A frontend developer uses APIs to fetch data. A backend developer writes APIs for other apps to use.\n\n"
                        "If you understand how to call an API, you are already halfway to building your first real software project! "
                        "You don't need expensive degrees to begin. Understanding how programs talk to each other is your superpower."
                    ),
                    examples=[
                        "Junior Developer building a simple Cricket Score app using a free Sports API.",
                        "AI Engineer connecting ChatGPT to WhatsApp via the WhatsApp Business API."
                    ],
                    callout_note="Career Tip: If you know how to connect APIs, you can build real products that solve real problems.",
                    key_terms=["Frontend-Backend Bridge", "Software Career", "Integration"]
                )
            ]

            practice_questions = [
                PracticeQuestion(
                    question="In the restaurant analogy, what role does the API play?",
                    options=[
                        "A) The Chef cooking the meal",
                        "B) The Waiter carrying orders between customer and kitchen",
                        "C) The Dining Table",
                        "D) The Cashier counting bills"
                    ],
                    answer="B",
                    explanation="The API acts as the waiter that takes your request to the server and returns the response."
                ),
                PracticeQuestion(
                    question="When you track a delivery driver on Zomato, what API is being used?",
                    options=[
                        "A) Google Maps API",
                        "B) Calculator API",
                        "C) Bluetooth API",
                        "D) Video Game API"
                    ],
                    answer="A",
                    explanation="Zomato displays map tracking by calling the Google Maps API."
                ),
                PracticeQuestion(
                    question="What are the two fundamental halves of any API communication?",
                    options=[
                        "A) Request and Response",
                        "B) Download and Delete",
                        "C) Restart and Sleep",
                        "D) Password and Username"
                    ],
                    answer="A",
                    explanation="A client sends a Request, and the server returns a Response."
                )
            ]

            takeaways = [
                "An API is like a restaurant waiter that connects apps together safely.",
                "Apps like Zomato, Uber, and GPay use APIs to access maps and bank servers.",
                "The two key steps are: Request (ordering) and Response (getting the result).",
                "APIs allow developers to reuse powerful tools without rebuilding from scratch.",
                "Mastering APIs is the foundation for web, mobile, and AI engineering careers."
            ]
        else:
            title = f"Beginner's Guide to {topic}"
            summary = f"A gentle, step-by-step introduction to {topic} designed for beginners starting from zero."
            core_analogy = f"Everyday Foundation for {topic}"
            key_concepts = [topic, "Basics", "Mechanism", "Application", "Career Relevance"]

            sections = [
                ContentSection(
                    title=plan.outline[0].title,
                    explanation=f"Welcome! Today we are exploring {topic}. Starting a career in modern technology can feel intimidating with heavy jargon, but at its heart, {topic} is based on simple, everyday ideas.",
                    examples=[f"Everyday Example: How {topic} appears in daily life."],
                    callout_note=f"Core Idea: {topic} solves real human problems.",
                    key_terms=[topic, "Foundations"]
                ),
                ContentSection(
                    title=plan.outline[1].title,
                    explanation=f"Let's look at how {topic} actually works behind the scenes.\n\n[DELIBERATE FLAW INJECTED ON DRAFT 1]: {topic} works by violating basic physical hardware constraints and using unexplained hyper-dimensional tensors without validation.",
                    examples=[f"Step-by-step walkthrough of {topic}."],
                    callout_note="Pay attention to the core sequence.",
                    key_terms=["Mechanism", "Step-by-Step"]
                ),
                ContentSection(
                    title=plan.outline[2].title,
                    explanation=f"Where is {topic} used in the real world? Companies in India and across the globe rely on {topic} to build scalable, reliable software.",
                    examples=[f"Industry use case for {topic}."],
                    callout_note="Practical impact is what matters in tech.",
                    key_terms=["Industry Use", "Practical Application"]
                ),
                ContentSection(
                    title=plan.outline[3].title,
                    explanation=f"Why should you care about {topic} for your career? Because understanding {topic} opens doors to entry-level software and AI roles.",
                    examples=[f"Career opportunities related to {topic}."],
                    callout_note="Keep building hands-on projects!",
                    key_terms=["Career Growth", "Next Steps"]
                )
            ]

            practice_questions = [
                PracticeQuestion(
                    question=f"What is the primary purpose of {topic}?",
                    options=[
                        "A) Solving a practical software problem in an accessible way",
                        "B) Making computers run slower",
                        "C) Replacing the human brain completely",
                        "D) Deleting all files"
                    ],
                    answer="A",
                    explanation=f"{topic} provides practical, structured solutions in modern computing."
                ),
                PracticeQuestion(
                    question=f"Who uses {topic} in industry?",
                    options=[
                        "A) Modern software companies, startups, and IT engineers",
                        "B) Nobody",
                        "C) Only antique collectors",
                        "D) Space aliens"
                    ],
                    answer="A",
                    explanation=f"Engineers across industries apply {topic} daily."
                )
            ]

            takeaways = [
                f"{topic} can be understood using simple everyday analogies.",
                "Focus on the problem it solves, not just the technical words.",
                "Practice with small examples to build your confidence."
            ]

        return EducationalContentSchema(
            title=title,
            topic=topic,
            target_audience=plan.target_audience,
            education_level=plan.education_level,
            summary=summary,
            core_analogy=core_analogy,
            key_concepts=key_concepts,
            sections=sections,
            practice_questions=practice_questions,
            key_takeaways=takeaways,
            references_and_further_reading=[
                f"Beginner's Guide to Modern Computing & {topic}",
                "Free Open-Source Interactive Tutorials",
                "Practical Hands-on Projects for Indian Students"
            ]
        )

    async def evaluate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan,
        quality_threshold: float
    ) -> EvaluationResult:
        await asyncio.sleep(1.0)

        # Check if deliberate flaw or unexplained jargon is present in content
        sec2_text = content.sections[1].explanation.lower()
        has_flaw = "[deliberate flaw" in sec2_text or "constantly retraining" in sec2_text or "kernel assembly" in sec2_text or "hyper-dimensional" in sec2_text

        checkpoints: List[RubricCheckpoint] = []

        if has_flaw:
            checkpoints.append(RubricCheckpoint(
                name="accurate_and_grounded",
                label="Accurate & Grounded",
                passed=False,
                reason=f"CRITICAL FACTUAL ERROR: Section 2 contains inaccurate claims that violate architectural principles."
            ))
            checkpoints.append(RubricCheckpoint(
                name="beginner_friendly_language",
                label="Beginner-Friendly Language",
                passed=False,
                reason="Language in Section 2 became overly academic and dense for a 12th-grade non-English-medium beginner."
            ))
            checkpoints.append(RubricCheckpoint(
                name="teaches_by_example",
                label="Teaches by Example",
                passed=True,
                reason=f"Excellently grounded in the relatable '{content.core_analogy}' analogy."
            ))
            checkpoints.append(RubricCheckpoint(
                name="no_unexplained_jargon",
                label="No Unexplained Jargon",
                passed=False,
                reason="JARGON DETECTED: Dense technical buzzwords were introduced without plain-English definitions."
            ))
            checkpoints.append(RubricCheckpoint(
                name="covers_key_points",
                label="Covers Key Points",
                passed=True,
                reason=f"Thoroughly covers: What is {content.topic}, Why it matters, and How it works."
            ))
            checkpoints.append(RubricCheckpoint(
                name="coherent_teaching_flow",
                label="Coherent Teaching Flow",
                passed=True,
                reason="Clear narrative flow ending with self-assessment questions."
            ))

            all_passed = False
            factual_accuracy = 65.0
            relevance = 92.0
            completeness = 80.0
            clarity_readability = 70.0
            educational_effectiveness = 70.0
            structure_organization = 85.0
            overall_score = round(
                (factual_accuracy * 0.25) +
                (relevance * 0.20) +
                (completeness * 0.20) +
                (clarity_readability * 0.15) +
                (educational_effectiveness * 0.10) +
                (structure_organization * 0.10),
                1
            )  # 76.7, below 80

            errors = [
                IdentifiedError(
                    section=content.sections[1].title,
                    severity="critical",
                    description=f"Factual inaccuracy and dense unexplained jargon in Section 2.",
                    unsupported_claim=True
                )
            ]
            missing = [f"Plain-English explanation of how {content.topic} operates without confusing buzzwords."]
            recs = [f"Remove dense jargon; anchor explanation completely in the '{content.core_analogy}'."]

            failed_names = [cp.label for cp in checkpoints if not cp.passed]
            memory_service.record_rejection_lesson(
                f"Keep language simple for {content.topic}; strip confusing jargon.",
                failed_names
            )
        else:
            checkpoints.append(RubricCheckpoint(
                name="accurate_and_grounded",
                label="Accurate & Grounded",
                passed=True,
                reason="All technical explanations are accurate and grounded."
            ))
            checkpoints.append(RubricCheckpoint(
                name="beginner_friendly_language",
                label="Beginner-Friendly Language",
                passed=True,
                reason="Vocabulary is clear and conversational for 12th-grade Indian learners."
            ))
            checkpoints.append(RubricCheckpoint(
                name="teaches_by_example",
                label="Teaches by Example",
                passed=True,
                reason=f"Excellently grounded in '{content.core_analogy}'."
            ))
            checkpoints.append(RubricCheckpoint(
                name="no_unexplained_jargon",
                label="No Unexplained Jargon",
                passed=True,
                reason="Zero unexplained jargon. Every acronym is translated immediately."
            ))
            checkpoints.append(RubricCheckpoint(
                name="covers_key_points",
                label="Covers Key Points",
                passed=True,
                reason="Covers What it is, Why it matters, and How it works."
            ))
            checkpoints.append(RubricCheckpoint(
                name="coherent_teaching_flow",
                label="Coherent Teaching Flow",
                passed=True,
                reason="Logical sequence with interactive check-your-understanding questions."
            ))

            all_passed = True
            factual_accuracy = 96.0
            relevance = 98.0
            completeness = 95.0
            clarity_readability = 94.0
            educational_effectiveness = 96.0
            structure_organization = 95.0
            overall_score = round(
                (factual_accuracy * 0.25) +
                (relevance * 0.20) +
                (completeness * 0.20) +
                (clarity_readability * 0.15) +
                (educational_effectiveness * 0.10) +
                (structure_organization * 0.10),
                1
            )
            errors = []
            missing = []
            recs = ["Content clears all 6 hard checkpoints with stellar pedagogical clarity."]

        return EvaluationResult(
            checkpoints=checkpoints,
            all_checkpoints_passed=all_passed,
            factual_accuracy=factual_accuracy,
            relevance=relevance,
            completeness=completeness,
            clarity_readability=clarity_readability,
            educational_effectiveness=educational_effectiveness,
            structure_organization=structure_organization,
            overall_score=overall_score,
            passed=all_passed,
            identified_errors=errors,
            missing_concepts=missing,
            improvement_recommendations=recs,
            unsupported_claims=[e.description for e in errors if e.unsupported_claim]
        )

    async def improve_content(
        self,
        content: EducationalContentSchema,
        evaluation: EvaluationResult,
        iteration: int
    ) -> ImprovementResult:
        await asyncio.sleep(1.0)

        topic = content.topic
        is_rag = "rag" in topic.lower()
        is_api = "api" in topic.lower()

        revised_sections = []
        modified_names = []

        for sec in content.sections:
            if "[deliberate flaw" in sec.explanation.lower() or sec == content.sections[1]:
                modified_names.append(sec.title)
                if is_rag:
                    cleaned = (
                        "This is where RAG comes in! RAG stands for Retrieval-Augmented Generation.\n\n"
                        "Now, instead of a closed-book exam, imagine the teacher tells you: 'You can bring your textbook into the exam hall.' "
                        "This is an Open-Book Exam. You don't have to memorize thousands of pages. You just need to know how to look up "
                        "the right topic in the index, read the paragraph, and write your answer.\n\n"
                        "Crucial Point to Remember (Common Interview Question!):\n"
                        "RAG does NOT change or retrain the AI model's internal brain (weights). The AI model stays completely untouched and frozen! "
                        "Instead, RAG acts like an intelligent assistant who runs to the library, photocopies the exact 2 pages you need, "
                        "and places them on your desk right beside your question paper. The AI reads those photocopied notes and writes the perfect answer."
                    )
                elif is_api:
                    cleaned = (
                        "You already use dozens of APIs every single day without realizing it!\n\n"
                        "1. **Food Delivery (Zomato / Swiggy):** Zomato doesn't own satellites in space. When you track your delivery driver on the map, "
                        "Zomato uses the **Google Maps API** to show the map.\n\n"
                        "2. **Online Payments (GPay / PhonePe / Paytm):** When you scan a QR code to pay ₹50 at a tea stall, the app uses a **Bank UPI API** "
                        "to securely ask the bank: 'Deduct ₹50 from my account and send it to the shopkeeper.'\n\n"
                        "Notice the magic: The Zomato app doesn't need to know how Google built satellites, and GPay doesn't need to know how the bank stores money. "
                        "They just ask the API politely, and the API brings back the answer."
                    )
                else:
                    cleaned = f"Let's look at how {topic} actually works in practice.\n\nIt works through clear, step-by-step communication where each component has a defined responsibility, ensuring reliable and secure results."

                revised_sections.append(ContentSection(
                    title=sec.title,
                    explanation=cleaned,
                    examples=sec.examples,
                    callout_note=sec.callout_note,
                    key_terms=sec.key_terms
                ))
            else:
                revised_sections.append(sec)

        revised_content = EducationalContentSchema(
            title=content.title,
            topic=content.topic,
            target_audience=content.target_audience,
            education_level=content.education_level,
            summary=content.summary + " (Remediated: All 6 hard quality checkpoints satisfied; zero jargon).",
            core_analogy=content.core_analogy,
            key_concepts=content.key_concepts,
            sections=revised_sections,
            practice_questions=content.practice_questions,
            key_takeaways=content.key_takeaways,
            references_and_further_reading=content.references_and_further_reading
        )

        failed_names = [cp.label for cp in evaluation.checkpoints if not cp.passed]
        changelog = (
            f"REJECTION LOG (Iteration {iteration}):\n"
            f"1. What Failed: Checkpoints [{', '.join(failed_names)}].\n"
            f"2. Why it Failed: Evaluator flagged factual inaccuracy and dense jargon in Section 2.\n"
            f"3. What was Changed: Completely removed flawed statements. Replaced with simple, conversational analogies ({content.core_analogy}) suitable for a 12th-grade Indian beginner."
        )

        return ImprovementResult(
            revised_content=revised_content,
            changelog=changelog,
            modified_sections=modified_names,
            improvements_applied=[
                f"Eliminated jargon and factual errors for {topic}",
                f"Grounded explanations in the '{content.core_analogy}'",
                "Simplified language for 12th-grade Indian student"
            ],
            rejection_resolution_summary=f"Resolved all {len(failed_names)} failed checkpoints from Pass {iteration}."
        )

    async def validate_content(
        self,
        content: EducationalContentSchema,
        plan: ContentPlan
    ) -> FinalValidationResult:
        await asyncio.sleep(0.7)

        return FinalValidationResult(
            passed=True,
            decision="APPROVED",
            factual_consistency_check=True,
            formatting_check=True,
            completeness_check=True,
            user_alignment_check=True,
            confidence_score=98.5,
            summary=f"Final QA audit passed: All 6 hard checkpoints cleared for '{content.topic}'. The lesson is completely grounded, beginner-accessible, and strictly free of unexplained jargon."
        )
