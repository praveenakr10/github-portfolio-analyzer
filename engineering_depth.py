def analyze_engineering_depth(repos):
    tech_stack = set()
    backend_keywords = ["django", "flask", "fastapi", "spring"]
    frontend_keywords = ["react", "vue", "angular"]
    database_keywords = ["sql", "mongodb", "postgres"]

    depth_score = 0

    for repo in repos:
        lang = repo.get("language")
        if lang:
            tech_stack.add(lang.lower())

        name = repo.get("name", "").lower()

        if any(k in name for k in backend_keywords):
            depth_score += 3
        if any(k in name for k in frontend_keywords):
            depth_score += 3
        if any(k in name for k in database_keywords):
            depth_score += 3

    diversity_bonus = min(len(tech_stack) * 2, 10)
    depth_score += diversity_bonus

    return min(depth_score, 15)
