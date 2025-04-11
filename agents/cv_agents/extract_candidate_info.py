# agents/cv_agents/extract_candidate_info.py
import json

def extract_info_from_summary(summary: str) -> dict:
    try:
        data = json.loads(summary)
    except:
        data = {}

    return {
        "full_name": data.get("full_name", "Unknown"),
        "email": data.get("email", "Unknown"),
        "techstack": data.get("techstack", "Not specified"),
        "experience": data.get("experience", "Unknown"),
        "skills": data.get("skills", "None listed")
    }
