from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter
from app.core.database import get_db
from app.models.commit import Commit

router = APIRouter(prefix="/api", tags=["analytics"])


@router.get("/leaderboard", summary="Rank all contributors by total commit count")
def get_leaderboard(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    total_contributors = db.query(Commit.author).distinct().count()

    offset = (page - 1) * limit
    results = (
        db.query(Commit.author, func.count(Commit.id).label("commit_count"))
        .group_by(Commit.author)
        .order_by(func.count(Commit.id).desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "page": page,
        "limit": limit,
        "total_contributors": total_contributors,
        "leaderboard": [
            {"rank": offset + i + 1, "author": author, "commits": count}
            for i, (author, count) in enumerate(results)
        ]
    }


@router.get("/heatmap/{username}", summary="Daily commit activity for one contributor")
def get_heatmap(username: str, db: Session = Depends(get_db)):
    commits = db.query(Commit).filter(Commit.author == username).all()
    if not commits:
        raise HTTPException(status_code=404, detail=f"No commits found for author '{username}'")

    counts = Counter(c.committed_at.date().isoformat() for c in commits if c.committed_at)
    return {"author": username, "commits_per_day": dict(sorted(counts.items()))}