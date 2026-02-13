import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
'''
def evaluate_readme(readme_text):
    if not readme_text:
        return {
            "readme_score": 0,
            "feedback": "No README found."
        }

    prompt = f"""
    You are a senior technical recruiter.

    Evaluate the following GitHub README.

    Score it out of 20 based on:
    - Clarity of problem statement
    - Setup instructions
    - Usage explanation
    - Real-world impact clarity

    Return:
    1. Score (just number)
    2. 3 strengths
    3. 3 improvement suggestions

    README:
    {readme_text[:3000]}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "ai_response": response.choices[0].message.content
    }

'''
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
def generate_growth_roadmap(username, total_score):
    prompt = f"""
    You are a senior software engineering mentor.

    GitHub Score: {total_score}/100

    Create a 30-day GitHub improvement roadmap divided into 4 weeks.

    Return ONLY valid JSON. No extra text.

    {{
      "week1": "",
      "week2": "",
      "week3": "",
      "week4": ""
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    import json

    raw_output = response.choices[0].message.content.strip()

    try:
        return json.loads(raw_output)
    except:
        return {
            "week1": "Improve README clarity and add setup instructions.",
            "week2": "Refactor commit messages and maintain steady commits.",
            "week3": "Deploy at least one project and add demo link.",
            "week4": "Add tests and improve documentation quality."
        }
