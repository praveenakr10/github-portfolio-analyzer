import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests

from github_service import (
    get_user_profile,
    get_user_repos,
    get_repo_readme,
    get_repo_commits
)
from scoring_engine import calculate_portfolio_score
from commit_analyzer import analyze_commit_patterns
from ai_evaluator import (
    evaluate_readme,
    recruiter_screening_summary,
    generate_growth_roadmap
)
from red_flag_engine import detect_red_flags
from engineering_depth import analyze_engineering_depth


st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")

st.title("🚀 GitHub Portfolio Analyzer")
st.markdown("AI-Powered Recruiter Style GitHub Evaluation")

st.markdown("""
### 🎯 What This Tool Does
- Evaluates GitHub from a recruiter’s perspective  
- Generates an objective portfolio score  
- Detects red flags  
- Highlights strongest projects  
- Provides a 30-day improvement roadmap  
""")

profile_input = st.text_input(
    "Enter GitHub Profile URL",
    placeholder="https://github.com/username"
)

if st.button("Analyze Profile") and profile_input:

    username = profile_input.rstrip("/").split("/")[-1]

    with st.spinner("Analyzing profile..."):

        profile = get_user_profile(username)

        if "error" in profile:
            st.error("GitHub user not found.")
            st.stop()

        repos = get_user_repos(username)

        # ---------- Score Calculation ----------
        score_data = calculate_portfolio_score(profile, repos)

        readme_text = None
        if repos:
            readme_text = get_repo_readme(username, repos[0]["name"])

        ai_result = evaluate_readme(readme_text)

        final_score = score_data["total_score"] + ai_result["readme_score"]
        final_score = min(final_score, 100)

        # ---------- Commit Analysis ----------
        commits = []
        if repos:
            commits = get_repo_commits(username, repos[0]["name"])

        commit_data = analyze_commit_patterns(commits)

        # ---------- Engineering Depth ----------
        engineering_score = analyze_engineering_depth(repos)

        # ---------- Red Flags ----------
        red_flags = detect_red_flags(profile, repos, commit_data, ai_result)

        # ---------- Recruiter Screening ----------
        recruiter_result = recruiter_screening_summary(
            username,
            final_score,
            score_data["breakdown"],
            ai_result
        )

        # ---------- Growth Roadmap ----------
        roadmap = generate_growth_roadmap(
            username,
            final_score,
            score_data["breakdown"],
            red_flags
        )

        # ---------- Highlighted Projects ----------
        top_repos = sorted(
            repos,
            key=lambda x: x.get("stargazers_count", 0),
            reverse=True
        )[:3]

        top_repositories = [
            {
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "description": repo["description"]
            }
            for repo in top_repos
        ]

        # ---------- Issue & PR Activity ----------
        repo_activity = []
        for repo in top_repos:
            issues_url = f"https://api.github.com/repos/{username}/{repo['name']}/issues"
            pulls_url = f"https://api.github.com/repos/{username}/{repo['name']}/pulls"

            issues = requests.get(issues_url).json()
            pulls = requests.get(pulls_url).json()

            repo_activity.append({
                "repo": repo["name"],
                "issues": len([i for i in issues if "pull_request" not in i]),
                "prs": len(pulls)
            })

    # ================= DISPLAY SECTION =================

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"👤 Username: {profile.get('login')}")

    with col2:
        st.metric("🎯 Portfolio Score", f"{final_score}/100")

    st.divider()

    # ---------- Highlighted Projects ----------
    st.subheader("🔝 Highlighted Projects")

    if top_repositories:
        for repo in top_repositories:
            st.markdown(f"### {repo['name']}")
            st.write(f"⭐ Stars: {repo['stars']}")
            st.write(f"🔤 Language: {repo['language']}")
            st.write(f"📝 {repo['description']}")
            st.markdown("---")
    else:
        st.info("No standout repositories detected.")

    # ---------- Issue & PR Activity ----------
    st.subheader("📬 Issue & PR Activity")

    for repo in repo_activity:
        st.markdown(f"### {repo['repo']}")
        st.write(f"Issues: {repo['issues']}")
        st.write(f"Pull Requests: {repo['prs']}")
        st.markdown("---")

    # ---------- Radar Chart ----------
    breakdown = score_data["breakdown"]

    categories = list(breakdown.keys())
    values = [min(v, 20) for v in breakdown.values()]

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8)

    st.subheader("📊 Score Breakdown")
    st.pyplot(fig)

    st.divider()

    # ---------- README ----------
    st.subheader("📄 README Evaluation")
    st.write(f"**README Score:** {ai_result['readme_score']}/20")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Strengths")
        for s in ai_result["strengths"]:
            st.write(f"- {s}")

    with col2:
        st.markdown("### 🔧 Improvements")
        for i in ai_result["improvements"]:
            st.write(f"- {i}")

    st.divider()

    # ---------- Recruiter Screening ----------
    st.subheader("🧠 Recruiter Screening Simulation")

    decision = recruiter_result["screening_decision"]

    if decision.lower() == "yes":
        st.success(f"✅ Screening Decision: {decision}")
    elif decision.lower() == "borderline":
        st.warning(f"⚠ Screening Decision: {decision}")
    else:
        st.error(f"❌ Screening Decision: {decision}")

    st.markdown("### 📋 Recruiter Summary")
    st.write(recruiter_result["recruiter_summary"])

    st.markdown("### 🚀 Top Improvements")
    for imp in recruiter_result["top_improvements"]:
        st.write(f"- {imp}")

    st.divider()

    # ---------- Commit Analysis ----------
    st.subheader("🛠 Commit Quality & Consistency Analysis")

    st.markdown("""
    **What this measures:**  
    This section evaluates how professionally the candidate manages version control.

    - Consistency Score → Measures regular development activity  
    - Message Quality Score → Evaluates clarity of commit messages  
    - Meaningless Commit Ratio → Detects vague commits like “update” or “fix”  
    - Burst Detection → Flags suspicious one-day commit dumps  
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📈 Consistency Score", f"{commit_data['consistency_score']}/15")

    with col2:
        st.metric("📝 Message Quality Score", f"{commit_data['message_quality_score']}/15")

    with col3:
        st.metric(
            "⚠ Meaningless Commit Ratio",
            f"{commit_data['meaningless_commit_ratio'] * 100}%"
        )

    if commit_data["burst_detected"]:
        st.error("🚩 Burst Commit Pattern Detected")
    else:
        st.success("✅ No burst commit pattern detected")

    st.divider()

    # ---------- Red Flags ----------
    st.subheader("🚩 Risk Flags")

    st.markdown("""
    **What this means:**  
    Red Flags are signals that recruiters consider risky:

    - Missing documentation  
    - Large inactivity gaps  
    - Too many forked repositories  
    - Low-quality commit history  
    - Very low public repository count  
    """)

    if red_flags:
        for flag in red_flags:
            st.error(f"⚠ {flag}")
    else:
        st.success("No major red flags detected.")

    st.divider()

    # ---------- Engineering Depth ----------
    st.subheader("🧠 Engineering Depth Score")

    st.markdown("""
    **What this measures:**  
    Engineering Depth evaluates real technical exposure:

    - Backend + frontend stack experience  
    - Database usage  
    - Technology diversity  
    - System-level project complexity  
    """)

    st.metric("Engineering Depth", f"{engineering_score}/15")

    st.divider()

    # ---------- Growth Plan ----------
    st.subheader("📅 30-Day GitHub Growth Plan")

    for week, content in roadmap.items():
        st.markdown(f"## {week.capitalize()}")
        st.markdown(f"**Focus:** {content.get('focus')}")

        for task in content.get("tasks", []):
            st.write(f"- {task}")
