import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

# Backend URL
API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="GitHub Portfolio Analyzer", layout="wide")

st.title("🚀 GitHub Portfolio Analyzer")
st.markdown("AI-Powered Recruiter Style GitHub Evaluation")

username = st.text_input("Enter GitHub Username")

if st.button("Analyze Profile") and username:

    with st.spinner("Analyzing profile..."):
        response = requests.get(f"{API_URL}/{username}")

    if response.status_code != 200:
        st.error("Error fetching data from backend.")
    else:
        data = response.json()

        # -------------------------
        # TOP SECTION
        # -------------------------
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"👤 Username: {data['username']}")

        with col2:
            score = data["github_portfolio_score"]
            st.metric("🎯 Portfolio Score", f"{score}/100")

        st.divider()

        # -------------------------
        # RADAR CHART
        # -------------------------
        breakdown = data["score_breakdown"]

        categories = list(breakdown.keys())
        values = list(breakdown.values())

        # Normalize to 100 scale visually
        max_values = [20] * len(categories)
        values = [min(v, 20) for v in values]

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

        # -------------------------
        # README EVALUATION
        # -------------------------
        st.subheader("📄 README Evaluation")

        readme_eval = data["readme_evaluation"]

        st.write(f"**README Score:** {readme_eval['readme_score']}/20")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Strengths")
            for s in readme_eval["strengths"]:
                st.write(f"- {s}")

        with col2:
            st.markdown("### 🔧 Improvements")
            for i in readme_eval["improvements"]:
                st.write(f"- {i}")

        st.divider()

        # -------------------------
        # RECRUITER SCREENING
        # -------------------------
        st.subheader("🧠 Recruiter Screening Simulation")

        screening = data["recruiter_screening"]

        decision = screening["screening_decision"]

        if decision.lower() == "yes":
            st.success(f"✅ Screening Decision: {decision}")
        elif decision.lower() == "borderline":
            st.warning(f"⚠ Screening Decision: {decision}")
        else:
            st.error(f"❌ Screening Decision: {decision}")

        st.markdown("### 📋 Recruiter Summary")
        st.write(screening["recruiter_summary"])

        st.markdown("### 🚀 Top Improvements")
        for imp in screening["top_improvements"]:
            st.write(f"- {imp}")

        st.divider()

        # -------------------------
        # COMMIT ANALYSIS SECTION
        # -------------------------
        st.subheader("🛠 Commit Quality & Consistency Analysis")

        commit_data = data.get("commit_analysis", {})

        if commit_data:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📈 Consistency Score", f"{commit_data['consistency_score']}/15")

            with col2:
                st.metric("📝 Message Quality Score", f"{commit_data['message_quality_score']}/15")

            with col3:
                ratio = commit_data["meaningless_commit_ratio"]
                st.metric("⚠ Meaningless Commit Ratio", f"{ratio * 100}%")

            if commit_data["burst_detected"]:
                st.error("🚩 Burst Commit Pattern Detected (Possible one-day dump)")
            else:
                st.success("✅ No burst commit pattern detected")

        else:
            st.warning("No commit data available.")
        st.divider()
        st.subheader("🚩 Risk Flags")
        st.markdown("""
        **What this means:**  
        Red Flags are signals that recruiters consider risky:
        - Missing documentation  
        - Low activity consistency  
        - Too many forked repos  
        - Poor commit quality  
        """)

        flags = data.get("red_flags", [])

        if flags:
            for f in flags:
                st.error(f"⚠ {f}")
        else:
            st.success("No major red flags detected. Profile shows stable signals.")

        st.divider()
        st.subheader("🧠 Engineering Depth Score")
        st.markdown("""
        **What this measures:**  
        Engineering Depth evaluates:
        - Backend + frontend exposure  
        - Database usage  
        - Technology stack diversity  
        - Real system-level thinking  
        """)

        st.metric("Engineering Depth", f"{data.get('engineering_depth_score', 0)}/15")
        st.divider()
        st.subheader("📅 30-Day GitHub Growth Plan")
        st.markdown("""
        **What this is:**  
        A personalized 4-week improvement roadmap to increase hiring readiness.
        """)

        roadmap = data.get("growth_roadmap", {})

        if roadmap:
            for week, tasks in roadmap.items():
                st.markdown(f"## {week.capitalize()}")

                if isinstance(tasks, dict):
                    for day_range, description in tasks.items():
                        st.markdown(f"**{day_range.replace('-', ' to ')}**")
                        st.write(f"- {description}")
                else:
                    st.info(tasks)

        else:
            st.warning("Roadmap could not be generated.")
