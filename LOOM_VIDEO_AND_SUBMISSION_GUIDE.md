# Loom Video & Submission Guide: GenAI Engineer Take-Home Assessment

This guide provides the exact 15–20 minute presentation script, screen walkthrough, and checklist to ace your submission for the **GenAI Engineer - Content Systems** role.

---

## 🎯 Submission Requirements Checklist

| Requirement | Artifact / Link | Where to Find in This Project |
| :--- | :--- | :--- |
| **1. GitHub Repo** | Your GitHub repository with code + setup instructions | Push this repository (`agentic-learning-system/`) |
| **2. Document Link** | Google Doc or Notion link containing the final lesson | Copy contents of `SUBMISSION_LESSON_RAG.md` into a Google Doc |
| **3. Loom Video** | 15–20 min face-visible video demonstrating workflow & deliberate error catching | Follow the script below |
| **4. Submission Form** | Official Google Form | [https://forms.gle/GKMb6wa7HiGFrXvC6](https://forms.gle/GKMb6wa7HiGFrXvC6) |

---

## 📹 15–20 Minute Loom Video Presentation Script

### Part 1: Introduction & Target Audience Context (0:00 – 3:00)
- **Face on Camera:** Introduce yourself warmly.
- **Problem Statement:** 
  > *"Hi everyone! In this video, I am walking you through my solution for the GenAI Engineer Take-Home Assessment. The goal is to build an autonomous Agentic Content System that plans, drafts, rigorously audits its own quality, and decides when content is good enough to ship—before any human ever sees it."*
- **Explain the Learner Persona:**
  > *"Our learner persona is very specific: A 12th-grade graduate from India with limited English vocabulary, a non-English-medium background, who starts from zero and wants to kickstart a career in AI. This means dense academic papers and unexplained mathematical jargon will fail them. The system must anchor concepts in everyday relatable analogies, like an Open-Book Exam versus a Closed-Book Exam."*

---

### Part 2: Architecture & Multi-Agent Design Walkthrough (3:00 – 6:30)
- **Show the Architecture Diagram / README:**
  > *"Instead of relying on a single clever prompt, I designed a compiled LangGraph state machine orchestrating 5 specialized agents:*
  > 1. **Content Planner Agent:** Ingests the 12th-grade Indian persona, selects the 'Open-Book Exam' analogy, and constructs the 3-pillar outline (What, Why, How).
  > 2. **Content Generator Agent:** Synthesizes clear, conversational explanations and interactive quiz questions.
  > 3. **Quality Evaluator Agent:** An independent auditor that judges content against a **6-checkpoint hard pass/fail rubric** (No partial credit).
  > 4. **Content Improvement Agent:** On rejection, isolates only the flawed sections, remediates errors, and records a structured Rejection Log.
  > 5. **Final Validation Agent:** Confirms that all 6 checkpoints pass before authorizing publication.
  >
  > *Across the pipeline, we have a **Self-Evolving Memory service** (`agent_memory.json`) that learns from rejections and dynamically sharpens future prompts."*

---

### Part 3: Live End-to-End Run & Catching a Deliberate Error (6:30 – 13:00)
**[CRITICAL ASSESSMENT REQUIREMENT: Catching a Deliberate Error]**

1. **Open the Dashboard (`http://127.0.0.1:5173`):**
   - Click **"Create Content"**.
   - Show that the preset is loaded with the official assessment topic: *"Introduction to RAG (Retrieval-Augmented Generation)"*.
   - Point out the **"Inject Deliberate Flaw (For Loom Video Evaluation Demo)"** toggle!
   - Explain to the viewer:
     > *"To prove that our evaluator is NOT a rubber stamp, I have enabled deliberate flaw injection. In Draft 1, the generator deliberately introduces two flaws:
     > 1) A factual misconception: claiming RAG retrains the model's neural weights on your PDFs.
     > 2) Dense, unexplained jargon: 'high-dimensional manifold cosine similarity embeddings'.
     > Let's watch the evaluator catch it."*

2. **Click "Run Agentic Workflow" & Watch Live Timeline:**
   - Watch the Planner complete, then Generator complete.
   - **Show the Evaluator Step:**
     - The Evaluator immediately catches the flaws!
     - Show the **FAIL Checkpoints** on screen:
       - `accurate_and_grounded: FAIL` (Flags that RAG does not retrain weights).
       - `no_unexplained_jargon: FAIL` (Flags 'manifold cosine similarity').
       - `beginner_friendly_language: FAIL`.
     - Show the score: **76.7 / 100 (< 80 threshold)** $\rightarrow$ **REJECTED**.
   - **Show the Rejection Log on screen:**
     - Point out the exact log entry: *What failed, Why it failed, and What needs to change*.

3. **Watch the Content Improvement Agent Remediate in Real-Time:**
   - The loop routes to the **Content Improver**.
   - It strips the weight-retraining claim, clarifies that **model weights remain 100% frozen**, and replaces mathematical jargon with the **"Doctor checking blood reports"** and **"Library photocopy"** analogies.
   - The loop re-enters the Evaluator for Pass 2:
     - All 6 checkpoints turn green: **PASS**!
     - Score jumps to **95.7 / 100** ($\ge 80$).
   - The **Final Validator** approves, and the curriculum is officially published!

---

### Part 4: Deep Dive into the Final Lesson & Rejection Log (13:00 – 16:30)
- Click **"Read Shipping Lesson"** to open the **Generated Content Reader**.
- Walk through the shipped lesson:
  - The **Closed-Book Exam** explanation of AI Hallucinations.
  - The **Open-Book Exam** explanation of RAG.
  - The **R - A - G** 3-step breakdown (Retrieve $\rightarrow$ Augment $\rightarrow$ Generate) using the redBus cancellation example.
  - The **Career Section** encouraging 12th-grade learners that 90% of real AI jobs in India involve RAG without needing a supercomputer.
  - Click on the interactive **Practice Quizzes** to show the hidden solutions and explanations.
- Click **"Revision History"** to display the side-by-side score delta (76.7 $\rightarrow$ 95.7).

---

### Part 5: Code Architecture, Trade-Offs & Conclusion (16:30 – 19:00)
- Briefly show the backend code in your editor:
  - `backend/app/agents/workflow.py` (LangGraph conditional routing).
  - `backend/app/providers/mock_provider.py` & `factory.py` (Supporting Mock, OpenAI, and Gemini).
  - `backend/app/services/memory_service.py` (Persistent self-evolving memory).
- **Discuss Architectural Trade-Offs:**
  - *Why Hard Pass/Fail Checkpoints?* In educational publishing for beginners, partial credit is dangerous—a lesson with 90% good prose but one critical factual misconception (like retraining weights) will confuse students forever.
  - *Why LangGraph?* Cyclic state machine support makes the generate $\rightarrow$ evaluate $\rightarrow$ regenerate loop natural, reproducible, and verifiable.
  - *Loop Termination Guarantee:* Max retries capped at 2 so execution always terminates.
- **Wrap up:** Thank the evaluation team and invite them to run the code locally using `run.bat` or inspect the repo.

