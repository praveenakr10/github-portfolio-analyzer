from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os
from github_service import get_user_profile, get_user_repos, get_repo_readme,get_repo_commits
from scoring_engine import calculate_portfolio_score
from commit_analyzer import analyze_commit_patterns
from ai_evaluator import evaluate_readme, recruiter_screening_summary, generate_growth_roadmap
from red_flag_engine import detect_red_flags
from engineering_depth import analyze_engineering_depth


load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "GitHub Portfolio Analyzer Running 🚀"}

@app.get("/test-groq")
def test_groq():
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
    messages=[
            {"role": "system", "content": "You are a recruiter."},
            {"role": "user", "content": "Say hello in one line."}
        ]
    )

    return {"response": response.choices[0].message.content}


@app.get("/analyze/{username}")
def analyze_user(username: str):
    profile = get_user_profile(username)
    repos = get_user_repos(username)

    score_data = calculate_portfolio_score(profile, repos)

    readme_text = None
    if repos:
        readme_text = get_repo_readme(username, repos[0]["name"])

    ai_result = evaluate_readme(readme_text)

    final_score = score_data["total_score"] + ai_result["readme_score"]
    final_score = min(final_score, 100)

    recruiter_result = recruiter_screening_summary(
        username,
        final_score,
        score_data["breakdown"],
        ai_result
    )
    
    commit_data = {}
    if repos:
        commits = get_repo_commits(username, repos[0]["name"])
        commit_data = analyze_commit_patterns(commits)
    engineering_score = analyze_engineering_depth(repos)

    red_flags = detect_red_flags(profile, repos, commit_data, ai_result)

    # Add engineering score to final score
    final_score += engineering_score
    final_score = min(final_score, 100)

    roadmap = generate_growth_roadmap(username, final_score)

    return {
    "username": profile.get("login"),
    "github_portfolio_score": final_score,
    "score_breakdown": score_data["breakdown"],
    "readme_evaluation": ai_result,
    "recruiter_screening": recruiter_result,
    "commit_analysis": commit_data,
    "engineering_depth_score": engineering_score,
    "red_flags": red_flags,
    "growth_roadmap": roadmap
    }



