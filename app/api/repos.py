from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from collections import Counter
from app.core.database import get_db
from app.services.github_service import fetch_commits, sync_commits
from app.models.commit import Commit
from app.models.repository import Repository


router = APIRouter(prefix="/api/repos", tags=["repos"])

@router.get("/{owner}/{repo}/commits")
def get_repo_commits(owner: str, repo: str, limit: int = 30):
    try:
        commits = fetch_commits(owner, repo, limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not fetch commits: {e}")
    return {"owner": owner, "repo": repo, "count": len(commits), "commits": commits}


@router.post("/{owner}/{repo}/sync")
def sync_repo_commits(owner: str, repo: str, limit: int = 30, db: Session = Depends(get_db)):
    try:
        saved = sync_commits(db, owner, repo, limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Sync failed: {e}")
    return {"owner": owner, "repo": repo, "new_commits_saved": len(saved)}


@router.get("/{owner}/{repo}/commits/stored")
def get_stored_commits(owner: str, repo: str, db: Session = Depends(get_db)):
    repository = db.query(Repository).filter(Repository.full_name == f"{owner}/{repo}").first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not synced yet — call /sync first")

    commits = db.query(Commit).filter(Commit.repository_id == repository.id).all()
    return {"owner": owner, "repo": repo, "count": len(commits), "commits": [
        {"sha": c.sha[:7], "author": c.author, "message": c.message, "date": c.committed_at}
        for c in commits
    ]}


@router.get("/{owner}/{repo}/activity")
def get_repo_activity(owner: str, repo: str, db: Session = Depends(get_db)):
    repository = db.query(Repository).filter(Repository.full_name == f"{owner}/{repo}").first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not synced yet — call /sync first")

    commits = db.query(Commit).filter(Commit.repository_id == repository.id).all()
    counts = Counter(c.committed_at.date().isoformat() for c in commits if c.committed_at)
    return {"owner": owner, "repo": repo, "commits_per_day": dict(sorted(counts.items()))}