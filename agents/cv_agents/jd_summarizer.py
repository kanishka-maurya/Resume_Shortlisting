# agents/cv_agents/jd_summarizer.py
from openai import OpenAI
import os

def summarize_jd(jd_text: str) -> str:
    # Dummy summarizer, replace with LLM API if needed
    return jd_text.strip()[:500]  # or use LLM for actual summary
