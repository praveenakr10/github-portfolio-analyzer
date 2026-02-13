from datetime import datetime


def analyze_commit_patterns(commits):
    """
    Analyze commit frequency and detect burst patterns
    """
    if not commits:
        return {
            "consistency_score": 0,
            "burst_detected": True,
            "message_quality_score": 0,
            "meaningless_commit_ratio": 1
        }

    commit_dates = []
    meaningful_count = 0
    meaningless_keywords = ["update", "fix", "changes", "minor", "test"]

    for commit in commits:
        date_str = commit["commit"]["author"]["date"]
        commit_dates.append(datetime.fromisoformat(date_str.replace("Z", "+00:00")))

        message = commit["commit"]["message"].lower()

        if not any(word in message for word in meaningless_keywords):
            meaningful_count += 1

    # Consistency calculation
    commit_dates.sort()
    gaps = []

    for i in range(1, len(commit_dates)):
        gap = (commit_dates[i] - commit_dates[i - 1]).days
        gaps.append(gap)

    max_gap = max(gaps) if gaps else 0

    consistency_score = max(0, 15 - max_gap)
    consistency_score = min(consistency_score, 15)

    # Burst detection (more than 5 commits in same day)
    date_counts = {}
    for d in commit_dates:
        day = d.date()
        date_counts[day] = date_counts.get(day, 0) + 1

    burst_detected = any(count > 5 for count in date_counts.values())

    meaningless_ratio = 1 - (meaningful_count / len(commits))
    message_quality_score = int((meaningful_count / len(commits)) * 15)

    return {
        "consistency_score": consistency_score,
        "burst_detected": burst_detected,
        "message_quality_score": message_quality_score,
        "meaningless_commit_ratio": round(meaningless_ratio, 2)
    }
