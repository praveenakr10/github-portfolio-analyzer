# GitHub Portfolio Analyzer & Enhancer

> **Transform your GitHub profile into a measurable career readiness signal**

An AI-powered evaluation engine that analyzes GitHub profiles from a recruiter's perspective, generating objective portfolio scores, technical insights, risk detection, and personalized 30-day improvement roadmaps.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://app-portfolio-analyzer-d6n7qdf7sufk2p3mwbm2zj.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 💡 The Problem

Recruiters spend countless hours manually evaluating GitHub profiles to assess:

-  Technical depth and expertise
-  Code quality and consistency
-  Real-world project impact
-  Professional development practices
-  Community engagement

**This process is subjective, time-consuming, and inconsistent.**

##  Solution

GitHub Portfolio Analyzer automates recruiter-style evaluation using **structured scoring algorithms** and **AI reasoning** to deliver actionable insights in seconds.

#### Demo Link: https://drive.google.com/file/d/1iMmFQ9fxQU7FRH4BBtAXbkWV_stWQvh8/view?usp=sharing
---

##  Key Features

###  Comprehensive Scoring System
- **Portfolio Score** (0-100): Objective evaluation across 9 key dimensions
- **Multi-factor analysis**: Repository quality, engagement, technical diversity, and more
- **Weighted scoring**: Prioritizes metrics that matter most to recruiters

###  AI-Powered Insights
- **README Quality Analysis**: LLM evaluation of documentation clarity and professionalism
- **Commit Pattern Analysis**: Detects consistency, message quality, and development habits
- **Recruiter Screening Simulation**: Yes/Borderline/No hiring decisions with detailed reasoning

###  Risk Detection
Automatically flags potential red flags:
- Missing or poor documentation
- Large inactivity gaps (>90 days)
- Excessive forked repositories
- Poor commit hygiene
- Minimal project portfolio

### 📈 30-Day Growth Roadmap
Personalized weekly action plan including:
- Repository restructuring strategies
- Commit hygiene improvement
- Engineering depth expansion
- Visibility and impact building
- Documentation enhancement

###  Deep Technical Analysis
- **Repository Highlights**: Showcases your strongest projects
- **Language Diversity**: Tracks technology stack breadth
- **Issue & PR Activity**: Measures collaboration and engagement
- **Engineering Depth**: Evaluates backend, frontend, and database experience

---

##  Architecture

```
User Input (GitHub URL)
        ↓
Streamlit Application (Frontend + Orchestration)
        ↓
GitHub REST API (Data Collection)
        ↓
Scoring Engine + Commit Analyzer
        ↓
Groq LLM (README Evaluation + Screening + Roadmap)
        ↓
Structured Recruiter-Style Report
```

---

##  Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend & Orchestration** | Streamlit |
| **API Integration** | GitHub REST API |
| **AI & LLM** | Groq API (LLaMA 3.1 8B Instant) |
| **Data Processing** | Python, NumPy |
| **Visualization** | Matplotlib |

---

##  Scoring Framework

| Component | Description | Weight |
|-----------|-------------|--------|
| **Repository Count** | Active project presence | High |
| **Followers Impact** | Community visibility | Medium |
| **Project Impact** | Stars and engagement metrics | High |
| **Technical Diversity** | Language and stack variety | Medium |
| **Original Projects** | Non-forked repository ratio | High |
| **README Quality** | AI-evaluated clarity and structure | High |
| **Commit Quality** | Consistency and message professionalism | High |
| **Engineering Depth** | Backend, frontend, database exposure | Medium |
| **Red Flags** | Risk detection signals | Critical |

---

##  Quick Start

### Prerequisites
- Python 3.8 or higher
- GitHub account
- Groq API key ([Get one here](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/praveenakr10/github-portfolio-analyzer.git

# Navigate to project directory
cd github-portfolio-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run dashboard.py
```

### Environment Setup

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY = "your_api_key_here"
```

Or set as environment variable:

```bash
export GROQ_API_KEY="your_api_key_here"
```

---

##  Live Demo

Try it now: [**GitHub Portfolio Analyzer**](https://app-portfolio-analyzer-d6n7qdf7sufk2p3mwbm2zj.streamlit.app/)

Simply enter any GitHub username to see instant analysis!

---

##  What Makes This Different

Unlike basic GitHub statistics dashboards, this system:

| Traditional Tools | Our Analyzer |
|-------------------|--------------|
| Shows basic stats | Evaluates from recruiter perspective |
| Displays numbers | Provides AI-powered qualitative assessment |
| Static metrics | Combines structured scoring with reasoning |
| No guidance | Generates actionable improvement roadmaps |
| Misses context | Detects hiring-risk patterns |

**We transform GitHub from a code hosting platform into a measurable career readiness signal.**

---

##  How It Works

### 1. **Data Collection**
Fetches comprehensive profile data via GitHub REST API:
- Repositories (public & contributions)
- Commit history and patterns
- Language distribution
- Engagement metrics (stars, forks, followers)

### 2. **Quantitative Analysis**
Applies weighted scoring algorithms across:
- Repository quality indicators
- Development consistency metrics
- Community impact signals
- Technical diversity measurements

### 3. **Qualitative AI Evaluation**
Leverages Groq's LLaMA 3.1 for:
- README content analysis
- Commit message quality assessment
- Recruiter screening simulation
- Personalized roadmap generation

### 4. **Report Generation**
Produces comprehensive analysis including:
- Overall portfolio score
- Detailed breakdowns by category
- Identified strengths and weaknesses
- Actionable improvement recommendations


## 🎯 Built For

This hackathon project focuses on:

- 🤖 **AI Integration**: Practical LLM applications in developer tooling
- 🛠️ **Developer Enablement**: Tools that help developers grow
- 💼 **Hiring Automation**: Streamlining technical recruitment
- 📈 **Career Growth**: Data-driven professional development

---

## 🗺️ Roadmap

- [ ] Support for GitLab and Bitbucket profiles
- [ ] Historical portfolio score tracking
- [ ] Team/organization analysis
- [ ] Peer comparison and benchmarking
- [ ] Integration with LinkedIn profiles
- [ ] Chrome extension for instant analysis
- [ ] API endpoint for programmatic access

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Praveena**
- GitHub: [@praveenakr10](https://github.com/praveenakr10)
- Project Link: [GitHub Portfolio Analyzer](https://github.com/praveenakr10/github-portfolio-analyzer)

---

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing fast LLM inference
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [GitHub API](https://docs.github.com/en/rest) for comprehensive developer data
- The open-source community for inspiration and support

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**


</div>
