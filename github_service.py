import requests

GITHUB_BASE_URL = "https://api.github.com"


def get_user_profile(username: str):
    """
    Fetch basic GitHub user profile data
    """
    url = f"{GITHUB_BASE_URL}/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "User not found"}


def get_user_repos(username: str):
    """
    Fetch public repositories of a user
    """
    url = f"{GITHUB_BASE_URL}/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_repo_readme(username: str, repo_name: str):
    """
    Fetch README content of a repository
    """
    url = f"{GITHUB_BASE_URL}/repos/{username}/{repo_name}/readme"
    headers = {
        "Accept": "application/vnd.github.v3.raw"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None


def get_repo_commits(username: str, repo_name: str):
    """
    Fetch recent commits of a repository (limited to 30)
    """
    url = f"{GITHUB_BASE_URL}/repos/{username}/{repo_name}/commits?per_page=30"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return []
