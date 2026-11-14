from typing import Dict, Any


def content_to_markdown(content_data: Dict[str, Any]) -> str:
    """
    Converts structured EducationalContent JSON into clean, publication-grade Markdown.
    """
    title = content_data.get("title", "Educational Guide")
    topic = content_data.get("topic", "")
    target_audience = content_data.get("target_audience", "")
    education_level = content_data.get("education_level", "")
    summary = content_data.get("summary", "")
    key_concepts = content_data.get("key_concepts", [])
    sections = content_data.get("sections", [])
    practice_questions = content_data.get("practice_questions", [])
    key_takeaways = content_data.get("key_takeaways", [])
    references = content_data.get("references_and_further_reading", [])

    lines = [
        f"# {title}\n",
        f"**Topic:** {topic}  ",
        f"**Target Audience:** {target_audience}  ",
        f"**Education Level:** {education_level}\n",
        "---\n",
        "## Executive Summary",
        f"{summary}\n",
        "### Key Concepts",
        ", ".join([f"`{c}`" for c in key_concepts]) + "\n\n",
        "---\n"
    ]

    # Sections
    for i, sec in enumerate(sections, 1):
        sec_title = sec.get("title", f"Section {i}")
        lines.append(f"## {i}. {sec_title}\n")
        lines.append(f"{sec.get('explanation', '')}\n")

        callout = sec.get("callout_note")
        if callout:
            lines.append(f"> [!NOTE]\n> {callout}\n")

        examples = sec.get("examples", [])
        if examples:
            lines.append("#### Illustrative Examples")
            for ex in examples:
                lines.append(f"- {ex}")
            lines.append("")

        terms = sec.get("key_terms", [])
        if terms:
            lines.append(f"*Key Terms:* {', '.join(terms)}\n")

        lines.append("")

    lines.append("---\n")

    # Practice Questions
    if practice_questions:
        lines.append("## Practice & Self-Assessment Questions\n")
        for i, q in enumerate(practice_questions, 1):
            lines.append(f"### Question {i}")
            lines.append(f"**{q.get('question', '')}**\n")
            opts = q.get("options", [])
            if opts:
                for opt in opts:
                    lines.append(f"- {opt}")
                lines.append("")
            lines.append(f"<details><summary><b>View Solution</b></summary>\n")
            lines.append(f"**Answer:** `{q.get('answer', '')}`\n")
            lines.append(f"**Explanation:** {q.get('explanation', '')}\n")
            lines.append("</details>\n")

    # Key Takeaways
    if key_takeaways:
        lines.append("## Key Takeaways\n")
        for item in key_takeaways:
            lines.append(f"- [x] {item}")
        lines.append("")

    # References
    if references:
        lines.append("## References & Further Reading\n")
        for ref in references:
            lines.append(f"1. {ref}")
        lines.append("")

    return "\n".join(lines)

