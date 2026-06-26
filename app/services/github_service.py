from github import Github, Auth
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.repository import Repository
from app.models.commit import Commit

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

def get_or_create_repository(db: Session, owner: str, repo: str) -> Repository:
    full_name = f"{owner}/{repo}"
    existing = db.query(Repository).filter(Repository.full_name == full_name).first()
    if existing:
        return existing

    new_repo = Repository(name=repo, owner=owner, full_name=full_name)
    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)
    return new_repo


def sync_commits(db: Session, owner: str, repo: str, limit: int = 30):
    client = get_github_client()
    repository_gh = client.get_repo(f"{owner}/{repo}")
    commits = repository_gh.get_commits()

    repository_db = get_or_create_repository(db, owner, repo)

    saved = []
    for commit in commits[:limit]:
        existing = db.query(Commit).filter(Commit.sha == commit.sha).first()
        if existing:
            continue  # already stored, skip duplicate

        author = commit.commit.author
        new_commit = Commit(
            sha=commit.sha,
            author=author.name if author else "unknown",
            message=commit.commit.message.split("\n")[0],
            committed_at=author.date if author else None,
            repository_id=repository_db.id,
        )
        db.add(new_commit)
        saved.append(new_commit)

    db.commit()
    return saved