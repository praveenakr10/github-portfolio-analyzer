def detect_red_flags(profile, repos, commit_data, readme_eval):
    flags = []

    # No README
    if readme_eval.get("readme_score", 0) == 0:
        flags.append("No proper README documentation detected.")

    # Too many forks
    forked = sum(1 for repo in repos if repo.get("fork"))
    if forked > len(repos) * 0.6:
        flags.append("Majority repositories are forked projects.")

    # Low consistency
    if commit_data.get("consistency_score", 0) < 5:
        flags.append("Large inactivity gaps detected in commits.")

    # High meaningless commit ratio
    if commit_data.get("meaningless_commit_ratio", 0) > 0.5:
        flags.append("High percentage of low-quality commit messages.")

    # Very low public repos
    if profile.get("public_repos", 0) < 3:
        flags.append("Very few public repositories.")

    return flags
