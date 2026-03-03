PAIN_SIGNAL_PROMPT_V1 = """
You are a startup opportunity analyst.

Task:
Determine whether the post indicates a real recurring pain point that could become an entrepreneur opportunity.

Return ONLY strict JSON with this exact schema:
{
  "is_pain_signal": boolean,
  "pain_signal_score": integer 0-10,
  "entrepreneur_opportunity_score": integer 0-10,
  "reasoning_short": string,
  "evidence_snippet": string
}

Rules:
- No markdown
- No extra keys
- Scores must be integers in range 0..10
""".strip()


def build_pain_signal_user_prompt(title: str, text: str = "") -> str:
    return (
        "Evaluate the following post.\n\n"
        f"TITLE:\n{title.strip()}\n\n"
        f"TEXT:\n{text.strip()}"
    ).strip()
