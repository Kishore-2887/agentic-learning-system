import os
import subprocess
import markdown

PROJECT_DIR = r"C:\Users\Kishore\.gemini\antigravity\scratch\agentic-learning-system"
OUTPUT_DIR = os.path.join(PROJECT_DIR, "downloadable_docs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
  
  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.65;
    color: #1e293b;
    background-color: #f8fafc;
    margin: 0;
    padding: 40px 20px;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    background: #ffffff;
    padding: 48px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    border: 1px solid #e2e8f0;
  }}
  h1 {{
    color: #0f172a;
    font-size: 28px;
    font-weight: 800;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 14px;
    margin-top: 0;
  }}
  h2 {{
    color: #1e293b;
    font-size: 22px;
    font-weight: 700;
    margin-top: 32px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 8px;
  }}
  h3 {{
    color: #334155;
    font-size: 18px;
    font-weight: 600;
    margin-top: 24px;
  }}
  p, li {{
    font-size: 15px;
    color: #334155;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 14px;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 10px 14px;
    text-align: left;
  }}
  th {{
    background-color: #f1f5f9;
    font-weight: 600;
    color: #0f172a;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  pre, code {{
    font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
    font-size: 13.5px;
  }}
  code {{
    background-color: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    color: #0f172a;
  }}
  pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 18px;
    border-radius: 8px;
    overflow-x: auto;
  }}
  pre code {{
    background-color: transparent;
    color: #38bdf8;
    padding: 0;
  }}
  blockquote {{
    border-left: 4px solid #3b82f6;
    background-color: #eff6ff;
    padding: 12px 20px;
    margin: 18px 0;
    border-radius: 0 8px 8px 0;
    color: #1e40af;
  }}
  a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
  }}
  a:hover {{
    text-decoration: underline;
  }}
  @media print {{
    body {{
      background: #ffffff;
      padding: 0;
    }}
    .container {{
      box-shadow: none;
      border: none;
      padding: 0;
      max-width: 100%;
    }}
  }}
</style>
</head>
<body>
<div class="container">
{content}
</div>
</body>
</html>
"""

DOCS = [
    {
        "md": "INTERVIEW_AND_SYSTEM_GUIDE.md",
        "title": "Master Interview, Setup & System Guide - Kishore",
        "base": "1_Interview_and_System_Guide"
    },
    {
        "md": "SUBMISSION_AND_VIDEO_CHECKLIST.md",
        "title": "Submission & Video Walkthrough Guide - Kishore",
        "base": "2_Submission_and_Video_Guide"
    },
    {
        "md": "SUBMISSION_LESSON_RAG.md",
        "title": "Final Lesson: Introduction to RAG - Kishore",
        "base": "3_Final_Lesson_RAG"
    }
]

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

for doc in DOCS:
    md_path = os.path.join(PROJECT_DIR, doc["md"])
    if not os.path.exists(md_path):
        continue
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    html_content = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    full_html = HTML_TEMPLATE.format(title=doc["title"], content=html_content)
    
    html_path = os.path.join(OUTPUT_DIR, f"{doc['base']}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated HTML: {html_path}")
    
    # Generate PDF using Microsoft Edge headless
    pdf_path = os.path.join(OUTPUT_DIR, f"{doc['base']}.pdf")
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        html_path
    ]
    try:
        subprocess.run(cmd, check=True, timeout=20)
        print(f"Generated PDF:  {pdf_path}")
    except Exception as e:
        print(f"Could not convert to PDF: {e}")

print("All docs converted successfully!")
