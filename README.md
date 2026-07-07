# DevPulse — Developer Activity & Productivity Tracker

A backend API that syncs GitHub commit data, stores it in PostgreSQL, and surfaces
developer activity metrics — leaderboards, heatmaps, and daily commit breakdowns.

Built as a portfolio project targeting the Bangladesh tech industry internship market.

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
│   ├── services/
│   │   └── github_service.py  # GitHub API logic
│   └── main.py                # FastAPI app entry point
├── tests/
│   └── test_main.py
├── alembic/                   # Database migrations
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

### 4. Start PostgreSQL with Docker

```bash
docker compose up -d
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

API is now live at `http://127.0.0.1:8000`  
Interactive docs at `http://127.0.0.1:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Confirm API is running |
| GET | `/health` | Health check |
| GET | `/db-check` | Database connection check |
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

## License

MIT © Md. Asibul Islam 2026