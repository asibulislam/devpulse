# DevPulse — Developer Activity & Productivity Tracker

A backend API that syncs GitHub commit data, stores it in PostgreSQL, and surfaces
developer activity metrics — leaderboards, heatmaps, and daily commit breakdowns.

Built as a portfolio project targeting the Bangladesh tech industry internship market.

**Live API:** https://devpulse-ya7b.onrender.com/docs

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

## Running Locally

### 1. Clone the repo

```bash
git clone git@github.com:asibulislam/devpulse.git
cd devpulse
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your real values:
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — any random string
- `GITHUB_TOKEN` — GitHub personal access token with `repo` scope

### 4. Start with Docker (recommended)

```bash
docker compose up --build
```

Both the API and PostgreSQL start together. Then run migrations:

```bash
docker exec devpulse_app alembic upgrade head
```

API is now live at `http://127.0.0.1:8000`
Interactive docs at `http://127.0.0.1:8000/docs`

### 5. Or run locally without Docker

```bash
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Confirm API is running |
| GET | `/health` | Health check |
| GET | `/db-check` | Database connection check |
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user profile |
| PATCH | `/api/auth/me` | Update github_username and email |
| GET | `/api/auth/me/stats` | Personal commit stats |
| POST | `/api/repos/{owner}/{repo}/sync` | Sync commits from GitHub to DB |
| GET | `/api/repos/{owner}/{repo}/commits` | Fetch live commits from GitHub |
| GET | `/api/repos/{owner}/{repo}/commits/stored` | List commits stored in DB |
| GET | `/api/repos/{owner}/{repo}/activity` | Daily commit breakdown for a repo |
| GET | `/api/leaderboard` | Rank contributors by total commits |
| GET | `/api/heatmap/{username}` | Daily activity breakdown for one person |

---

## Running Tests

```bash
pytest
```

---

## License

MIT © Md. Asibul Islam 2026