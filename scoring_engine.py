def calculate_portfolio_score(profile, repos):
    """
    Calculate a structured GitHub Portfolio Score (out of 100)
    """

    score = 0
    breakdown = {}

    repo_points = min(profile.get("public_repos", 0), 15)
    score += repo_points

    follower_points = min(profile.get("followers", 0) // 10, 10)
    score += follower_points

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos[:5])
    star_points = min(total_stars // 50, 20)
    score += star_points


    languages = set(repo.get("language") for repo in repos if repo.get("language"))
    language_points = min(len(languages) * 3, 15)
    score += language_points

    active_repos = sum(1 for repo in repos if not repo.get("fork"))
    active_points = min(active_repos * 2, 20)
    score += active_points

    breakdown["ai_evaluation_reserved"] = 20
    breakdown["Repository Organization"] = repo_points
    breakdown["Impact & Visibility"] = follower_points + star_points
    breakdown["Project Impact"] = star_points
    breakdown["Technical Depth"] = language_points
    breakdown["Original Work Ratio"] = active_points

    return {
        "total_score": min(score, 100),
        "breakdown": breakdown
    }


