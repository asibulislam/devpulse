from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from collections import Counter
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.user import User
from app.models.commit import Commit
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.token import TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/register", response_model=UserResponse, summary="Register a new user")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == form_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=form_data.username,
        hashed_password=hash_password(form_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse, summary="Login and get access token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse, summary="Get current logged-in user")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse, summary="Update your profile")
def update_me(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if update_data.github_username is not None:
        existing = db.query(User).filter(
            User.github_username == update_data.github_username,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="github_username already taken")
        current_user.github_username = update_data.github_username

    if update_data.email is not None:
        existing = db.query(User).filter(
            User.email == update_data.email,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")
        current_user.email = update_data.email

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/stats", summary="Get your personal commit stats")
def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.github_username:
        raise HTTPException(
            status_code=400,
            detail="Set your github_username first via PATCH /api/auth/me"
        )

    commits = db.query(Commit).filter(
        Commit.author == current_user.github_username
    ).all()

    if not commits:
        return {
            "username": current_user.username,
            "github_username": current_user.github_username,
            "total_commits": 0,
            "commits_per_day": {},
            "repos_contributed": []
        }

    counts = Counter(
        c.committed_at.date().isoformat() for c in commits if c.committed_at
    )

    repo_ids = list(set(c.repository_id for c in commits))

    from app.models.repository import Repository
    repos = db.query(Repository).filter(Repository.id.in_(repo_ids)).all()

    return {
        "username": current_user.username,
        "github_username": current_user.github_username,
        "total_commits": len(commits),
        "commits_per_day": dict(sorted(counts.items())),
        "repos_contributed": [r.full_name for r in repos]
    }