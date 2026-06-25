from fastapi import APIRouter, HTTPException
from app.services.github_service import fetch_commits

router = APIRouter(prefix="/api/repos", tags=["repos"])

@router.get("/{owner}/{repo}/commits")
def get_repo_commits(owner: str, repo: str, limit: int = 30):
    try:
        commits = fetch_commits(owner, repo, limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not fetch commits: {e}")
    return {"owner": owner, "repo": repo, "count": len(commits), "commits": commits}