import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
print("GROQ KEY:", os.getenv("GROQ_API_KEY"))

def evaluate_readme(readme_text):
    if not readme_text:
        return {
            "readme_score": 0,
            "strengths": [],
            "improvements": ["No README found."]
        }

    prompt = f"""
    You are a senior technical recruiter.

    Evaluate the following GitHub README.

    Score it STRICTLY out of 20.

    Return ONLY valid JSON in this format:

    {{
      "readme_score": number,
      "strengths": ["point1", "point2", "point3"],
      "improvements": ["point1", "point2", "point3"]
    }}

    README:
    {readme_text[:3000]}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    import json

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {
            "readme_score": 0,
            "strengths": [],
            "improvements": ["AI response parsing failed."]
        }


def recruiter_screening_summary(username, total_score, breakdown, readme_eval):
    prompt = f"""
    You are a senior technical recruiter at a product-based company.

    Candidate GitHub Username: {username}
    Overall Score: {total_score}/100
    Score Breakdown: {breakdown}
    README Evaluation: {readme_eval}

    Based on this, answer:

    1. Would this candidate PASS initial GitHub screening? (Yes / Borderline / No)
    2. Short recruiter summary (4-5 lines)
    3. Top 3 improvements to increase hiring chances

    Return ONLY valid JSON:

    {{
      "screening_decision": "",
      "recruiter_summary": "",
      "top_improvements": ["", "", ""]
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    import json

    try:
        return json.loads(response.choices[0].message.content)
    except:
        return {
            "screening_decision": "Unknown",
            "recruiter_summary": "AI parsing failed.",
            "top_improvements": []
        }
def generate_growth_roadmap(username, total_score, breakdown=None, red_flags=None):
    prompt = f"""
        You are a senior software engineering mentor helping a student improve their GitHub profile.

        GitHub Score: {total_score}/100
        Score Breakdown: {breakdown}
        Detected Red Flags: {red_flags}

        Create a concise, practical 30-day improvement roadmap.

        Rules:
        - Divide into exactly 4 weeks.
        - Each week must have:
            - A clear focus title
            - 3 to 4 specific, actionable tasks
        - Do NOT create daily plans.
        - Do NOT break into 2-day schedules.
        - Keep it structured and professional.
        - Tasks must be measurable (e.g., "Add architecture diagram to README", "Refactor 3 weak commit messages")

        Return ONLY valid JSON in this format:

        {{
        "week1": {{
            "focus": "",
            "tasks": ["", "", ""]
        }},
        "week2": {{
            "focus": "",
            "tasks": ["", "", ""]
        }},
        "week3": {{
            "focus": "",
            "tasks": ["", "", ""]
        }},
        "week4": {{
            "focus": "",
            "tasks": ["", "", ""]
        }}
        }}
        """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        import json, re

        raw_output = response.choices[0].message.content.strip()

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

    except Exception:
        pass

    # Safe fallback (clean and structured)
    return {
        "week1": {
            "focus": "Improve Documentation & Presentation",
            "tasks": [
                "Rewrite README with clear problem statement and impact section",
                "Add setup instructions and usage examples",
                "Include architecture diagram or workflow explanation"
            ]
        },
        "week2": {
            "focus": "Strengthen Project Quality",
            "tasks": [
                "Refactor code for better structure and modularity",
                "Add meaningful commit messages",
                "Remove or archive low-quality repositories"
            ]
        },
        "week3": {
            "focus": "Increase Technical Depth",
            "tasks": [
                "Add backend + database integration to one project",
                "Deploy one project and include live demo link",
                "Introduce basic testing framework"
            ]
        },
        "week4": {
            "focus": "Improve Recruiter Signaling",
            "tasks": [
                "Pin strongest 3 repositories",
                "Add measurable outcomes in project descriptions",
                "Maintain consistent commit activity"
            ]
        }
    }
