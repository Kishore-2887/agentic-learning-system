# 🎬 Complete Submission & Video Demonstration Guide
## GenAI Engineer - Content Systems | Take-Home Assessment

> **Official Submission Form:** [https://forms.gle/GKMb6wa7HiGFrXvC6](https://forms.gle/GKMb6wa7HiGFrXvC6)  
> **Your GitHub Repo:** [https://github.com/Kishore-2887/agentic-learning-system](https://github.com/Kishore-2887/agentic-learning-system)

---

## 📋 The 3 Deliverables You Must Submit

When you open the Google Submission Form, you will be asked for **3 links**:

| Deliverable | What it is | Status | Link / Location |
|---|---|---|---|
| **1. GitHub Repo** | Agentic workflow code + README with setup & run steps | ✅ **Ready** | `https://github.com/Kishore-2887/agentic-learning-system` |
| **2. Document Link** | Final lesson content + Rejection Log (Google Doc / Notion) | 📝 **Ready to Copy** | Copy from `SUBMISSION_LESSON_RAG.md` into Google Docs |
| **3. Loom Video** | 15–20 min face-visible walkthrough | 🎥 **Ready to Record** | Follow the minute-by-minute script below |

---

## 📄 Step 1: Create Your Google Doc (Takes 3 Minutes)

1. Open your browser and go to **[docs.google.com](https://docs.google.com)** $\rightarrow$ Create a **Blank Document**.
2. Name the document: `GenAI Content Systems - Introduction to RAG Lesson & Rejection Log`.
3. Open the file **`SUBMISSION_LESSON_RAG.md`** in your project folder, copy all text (`Ctrl + A`, `Ctrl + C`), and paste it into your Google Doc (`Ctrl + V`).
4. **Crucial Sharing Step**:
   * Click the blue **Share** button in the top right corner.
   * Under *General Access*, change from **Restricted** to **"Anyone with the link can view"**.
   * Click **Copy Link**. Keep this link ready!

---

## 🎥 Step 2: Loom Video Requirements

The assessment explicitly lists these **3 mandatory video rules**:
1. **Duration:** 15 to 20 minutes.
2. **Camera:** Your **face must be visible** (use Loom's circular webcam bubble in the corner).
3. **Content to Cover:**
   * Your agentic workflow running end-to-end.
   * Your evaluator catching a deliberate error on camera.
   * A walkthrough of how your workflow and architecture work.

---

## ⏱️ Minute-by-Minute Loom Video Script (Follow This!)

### 📌 Minutes 0:00 – 2:30 | Introduction & Candidate Persona
* **What to show on screen:** Your face camera + your GitHub repository page.
* **What to say:**
  > *"Hello! My name is Kishore. Today I am presenting my solution for the GenAI Engineer - Content Systems take-home assessment.
  > 
  > The problem statement asks us to build an autonomous agentic system that generates learning content and evaluates its own quality before a human ever sees it. 
  > 
  > Our target learner is a 12th-grade graduate from India with limited English vocabulary, a non-English-medium background, starting from zero to kickstart an AI career. 
  > 
  > Today, our system will generate a complete beginner lesson for 'Introduction to RAG (Retrieval-Augmented Generation)'."*

---

### 📌 Minutes 2:30 – 6:00 | Architecture & Design Choices
* **What to show on screen:** Open `README.md` or `INTERVIEW_AND_SYSTEM_GUIDE.md` showing the flowchart.
* **What to say:**
  > *"Instead of writing a single prompt with ChatGPT—which is prone to hallucinations and dense jargon—we designed a multi-agent state machine using **LangGraph** in Python.
  > 
  > Why LangGraph? Because standard LangChain chains only move forward in a straight line. But educational generation requires **cycles and feedback loops**: Generate $\rightarrow$ Evaluate $\rightarrow$ if failed, Remediate $\rightarrow$ Re-evaluate.
  > 
  > We have 5 specialized agents:
  > 1. **Content Planner Agent**: Analyzes the learner persona and selects culturally relatable analogies, like 'Open-Book Exam vs. Closed-Book Exam'.
  > 2. **Content Generator Agent**: Drafts the curriculum.
  > 3. **Quality Evaluator Agent**: Acts as an automated gatekeeper testing against 6 hard pass/fail checkpoints with zero partial credit.
  > 4. **Content Improver Agent**: Reads the rejection feedback and rewrites flawed sections.
  > 5. **Validation Agent**: Confirms zero jargon and compliance before publishing."*

---

### 📌 Minutes 6:00 – 11:30 | Live End-to-End Run & Catching the Deliberate Error (Crucial!)
* **What to show on screen:** Open your terminal in VS Code.
* **Action to take:**
  Type in the terminal and press Enter:
  ```powershell
  python run_cli.py
  ```
* **What to explain as it runs:**
  > *"Now, let's watch the agentic loop run end-to-end in real-time.
  > 
  > **Step 1:** The Planner agent selected the 'Open-Book Exam' analogy.
  > 
  > **Step 2:** The Generator drafted Draft 1. Notice here on screen: to rigorously test our evaluator, Draft 1 was injected with a deliberate factual error—it claims RAG retrains neural network weights on every query, and it injected dense jargon like 'manifold cosine similarity'.
  > 
  > **Step 3 - The Evaluator catches it:** Look at the screen right here:
  > - Checkpoint 1 (Accurate & Grounded) $\rightarrow$ **FAIL!** The evaluator flagged: 'Section 2 claims RAG constantly retrains neural network weights. RAG does NOT retrain weights; it supplies retrieved text into prompt context.'
  > - Checkpoint 2 (Beginner-Friendly Language) $\rightarrow$ **FAIL!**
  > - Checkpoint 4 (No Unexplained Jargon) $\rightarrow$ **FAIL!** Detected 'manifold cosine similarity'.
  > 
  > Because we use hard checkpoints without partial credit, the overall score is 76.7/100, and the Evaluator issues a **REJECTION** and triggers the Content Improvement Agent.
  > 
  > **Step 4 - Self-Correction:** The Improver agent reads the rejection log, completely removes the weight-retraining error, clarifies that AI weights remain 100% frozen, and replaces math terms with the 'Library Photocopy' analogy.
  > 
  > **Step 5 - Pass #2:** The Evaluator re-grades Draft 2, and all 6 checkpoints turn green **PASS** with a score of 95.8/100!
  > 
  > **Step 6 & 7:** The Validation agent signs off, and the curriculum is officially shipped."*

---

### 📌 Minutes 11:30 – 16:00 | Walkthrough of Code & Engineering Rigor
* **What to show on screen:** Show the code files in VS Code sidebar:
  * `backend/app/agents/workflow.py` $\rightarrow$ Show the LangGraph state machine and conditional edges.
  * `backend/app/agents/evaluator.py` $\rightarrow$ Show the 6 boolean checkpoints.
  * `backend/app/providers/factory.py` $\rightarrow$ Show how easy it is to switch between Mock, OpenAI GPT-4o, and Google Gemini.
* **Run automated unit tests live:**
  In terminal, run:
  ```powershell
  python -m pytest backend/tests/ -v
  ```
  Show the examiner that **all 10/10 automated tests pass**.

---

### 📌 Minutes 16:00 – 20:00 | Final Curriculum Review & Wrap-up
* **What to show on screen:** Open your created Google Doc showing the final lesson.
* **What to say:**
  > *"Here is the final generated lesson that cleared all quality gates:
  > - Section 1 explains AI Hallucination using the relatable 12th board exam analogy.
  > - Section 2 explains RAG using the Open-Book Exam secret, explicitly clarifying that AI weights remain untouched.
  > - Section 3 breaks down R-A-G into Retrieve, Augment, Generate.
  > - Section 4 explains the career value for Indian students.
  > - And it concludes with a 3-question self-assessment quiz.
  > 
  > To ensure reliability across environments, we included 1-click batch scripts (`setup.bat` and `start.bat`) so anyone can clone and run this on any laptop in minutes.
  > 
  > Thank you for reviewing my assessment! All code is live on GitHub, and the links are submitted in the form."*

---

## 🚀 Step 3: Fill Out the Submission Form

Go to: **[https://forms.gle/GKMb6wa7HiGFrXvC6](https://forms.gle/GKMb6wa7HiGFrXvC6)**

Fill out the fields:
1. **GitHub Repository Link:**
   ```text
   https://github.com/Kishore-2887/agentic-learning-system
   ```
2. **Document Link:**
   *(Paste your Google Doc link with "Anyone with link can view" access)*
3. **Loom Video Link:**
   *(Paste your completed Loom video link)*
4. Click **Submit**!
