from github import Github, Auth
from app.core.config import settings

def get_github_client() -> Github:
    auth = Auth.Token(settings.github_token)
    return Github(auth=auth)

def fetch_commits(owner: str, repo: str, limit: int = 30):
    client = get_github_client()
    repository = client.get_repo(f"{owner}/{repo}")
    commits = repository.get_commits()

    result = []
    for commit in commits[:limit]:
        author = commit.commit.author
        result.append({
            "sha": commit.sha[:7],
            "author": author.name if author else "unknown",
            "message": commit.commit.message.split("\n")[0],
            "date": author.date.isoformat() if author else None,
            "url": commit.html_url,
        })
    return result