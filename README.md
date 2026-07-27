# DevPulse — Developer Activity & Productivity Tracker

A backend API that syncs GitHub commit data, stores it in PostgreSQL, and surfaces
developer activity metrics — leaderboards, heatmaps, and daily commit breakdowns.

Built to demonstrate REST API design, relational data modeling, and third-party
API integration in a production-style backend service.

**Live API:** https://devpulse-ya7b.onrender.com/docs

**Live Dashboard:** https://asibulislam-devpulse.streamlit.app

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Database | PostgreSQL 16 (Docker) |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| GitHub Integration | PyGithub |
| Testing | pytest + httpx |
| Config | pydantic-settings |
| Deployment | Render |

---

## Project Structure

```
devpulse/
├── app/
│   ├── api/
│   │   ├── repos.py           # Repo sync + commit endpoints
│   │   └── analytics.py       # Leaderboard + heatmap endpoints
│   ├── core/
│   │   ├── config.py          # Environment variable loading
│   │   └── database.py        # SQLAlchemy engine + session
│   ├── models/
│   │   ├── user.py            # User model
│   │   ├── repository.py      # Repository model
│   │   └── commit.py          # Commit model
│   ├── schemas/
│   │   ├── user.py            # User input/output schemas
│   │   ├── commit.py          # Commit response schema
│   │   └── token.py           # Token response schema
│   ├── services/
│   │   └── github_service.py  # GitHub API logic
│   └── main.py                # FastAPI app entry point
├── tests/
│   ├── conftest.py            # Test fixtures and shared setup
│   ├── test_main.py           # Root and health endpoint tests
│   ├── test_auth.py           # Auth flow tests
│   ├── test_repos.py          # Repo endpoint tests
│   └── test_analytics.py     # Analytics endpoint tests
├── alembic/                   # Database migrations
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:asibulislam/devpulse.git
cd devpulse
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and provide values for:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — a random secret string
- `GITHUB_TOKEN` — a GitHub personal access token with `repo` scope

### 4. Run with Docker (recommended)

```bash
docker compose up --build
```

This starts the API and PostgreSQL together. Then apply migrations:

```bash
docker exec devpulse_app alembic upgrade head
```

The API is now available at `http://127.0.0.1:8000`, with interactive
documentation at `http://127.0.0.1:8000/docs`.

### 5. Run without Docker

```bash
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Confirm the API is running |
| GET | `/health` | Health check |
| GET | `/db-check` | Database connection check |
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Log in and receive a JWT token |
| GET | `/api/auth/me` | Get the current user's profile |
| PATCH | `/api/auth/me` | Update `github_username` and `email` |
| GET | `/api/auth/me/stats` | Retrieve personal commit statistics |
| POST | `/api/repos/{owner}/{repo}/sync` | Sync commits from GitHub into the database |
| GET | `/api/repos/{owner}/{repo}/commits` | Fetch live commits from GitHub |
| GET | `/api/repos/{owner}/{repo}/commits/stored` | List commits stored in the database |
| GET | `/api/repos/{owner}/{repo}/activity` | Daily commit breakdown for a repository |
| GET | `/api/leaderboard` | Rank contributors by total commits |
| GET | `/api/heatmap/{username}` | Daily activity breakdown for a single user |

---

## Running Tests

```bash
pytest
```

---

## License

MIT © Md. Asibul Islam, 2026