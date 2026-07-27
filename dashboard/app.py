import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

API_BASE = "https://devpulse-ya7b.onrender.com"

st.set_page_config(
    page_title="DevPulse Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ── Custom CSS ──
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1B4F72;
        text-align: center;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f4f8;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown('<p class="main-header">⚡ DevPulse</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Developer Activity & Productivity Tracker</p>', unsafe_allow_html=True)
st.markdown("---")

# ── Sidebar ──
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Leaderboard", "Developer Heatmap", "Repo Activity", "Login"])
st.sidebar.markdown("---")
st.sidebar.markdown(f"**API:** [{API_BASE}]({API_BASE}/docs)")
st.sidebar.markdown("**GitHub:** [asibulislam/devpulse](https://github.com/asibulislam/devpulse)")


# PAGE 1 — LEADERBOARD
if page == "Leaderboard":
    st.header("🏆 Contributor Leaderboard")
    st.caption("Top developers ranked by total commit count across all synced repositories.")

    try:
        resp = requests.get(f"{API_BASE}/api/leaderboard?page=1&limit=20", timeout=15)
        data = resp.json()

        if resp.status_code == 200 and data.get("leaderboard"):
            lb = data["leaderboard"]

            # Metrics row
            col1, col2 = st.columns(2)
            col1.metric("Total Contributors", data.get("total_contributors", 0))
            col2.metric("Showing", len(lb))

            # Bar chart
            authors = [entry["author"] for entry in lb]
            commits = [entry["commits"] for entry in lb]

            fig = px.bar(
                x=commits,
                y=authors,
                orientation="h",
                labels={"x": "Total Commits", "y": "Contributor"},
                title="Commits by Contributor",
                color=commits,
                color_continuous_scale="Blues",
            )
            fig.update_layout(
                yaxis=dict(autorange="reversed"),
                showlegend=False,
                height=max(300, len(lb) * 40),
                margin=dict(l=10, r=10, t=40, b=10),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Table
            st.subheader("Full Rankings")
            st.dataframe(
                {
                    "Rank": [e["rank"] for e in lb],
                    "Contributor": [e["author"] for e in lb],
                    "Commits": [e["commits"] for e in lb],
                },
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning("No leaderboard data yet. Sync a repository first.")

    except Exception as e:
        st.error(f"Could not reach the API. It may be waking up (free tier). Try again in 30 seconds.\n\n{e}")

# PAGE 2 — DEVELOPER HEATMAP

elif page == "Developer Heatmap":
    st.header("🔥 Developer Activity Heatmap")
    st.caption("Daily commit breakdown for any contributor.")

    username = st.text_input("Enter contributor name (as it appears in Git commits)", placeholder="e.g. Asibul Islam")

    if username:
        try:
            resp = requests.get(f"{API_BASE}/api/heatmap/{username}", timeout=15)
            data = resp.json()

            if resp.status_code == 200:
                cpd = data.get("commits_per_day", {})

                if cpd:
                    dates = list(cpd.keys())
                    counts = list(cpd.values())

                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Commits", sum(counts))
                    col2.metric("Active Days", len(dates))
                    col3.metric("Peak Day", max(counts))

                    # Line chart
                    fig = px.bar(
                        x=dates,
                        y=counts,
                        labels={"x": "Date", "y": "Commits"},
                        title=f"Daily Commit Activity — {username}",
                        color=counts,
                        color_continuous_scale="Teal",
                    )
                    fig.update_layout(
                        showlegend=False,
                        coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=40, b=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Table
                    st.subheader("Daily Breakdown")
                    st.dataframe(
                        {"Date": dates, "Commits": counts},
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No commit data found for this contributor.")
            else:
                st.error(data.get("detail", "Contributor not found."))

        except Exception as e:
            st.error(f"Could not reach the API. Try again in 30 seconds.\n\n{e}")

# PAGE 3 — REPO ACTIVITY

elif page == "Repo Activity":
    st.header("📁 Repository Activity")
    st.caption("View commit history and daily activity for any synced repository.")

    col1, col2 = st.columns(2)
    owner = col1.text_input("GitHub Owner", placeholder="e.g. asibulislam")
    repo  = col2.text_input("Repository Name", placeholder="e.g. devpulse")

    if owner and repo:
        try:
            # Activity chart
            resp = requests.get(f"{API_BASE}/api/repos/{owner}/{repo}/activity", timeout=15)
            data = resp.json()

            if resp.status_code == 200:
                cpd = data.get("commits_per_day", {})
                if cpd:
                    dates  = list(cpd.keys())
                    counts = list(cpd.values())

                    col1, col2 = st.columns(2)
                    col1.metric("Total Commits", sum(counts))
                    col2.metric("Active Days", len(dates))

                    fig = px.area(
                        x=dates, y=counts,
                        labels={"x": "Date", "y": "Commits"},
                        title=f"Daily Activity — {owner}/{repo}",
                        color_discrete_sequence=["#1B4F72"],
                    )
                    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No activity data yet.")
            else:
                st.error(data.get("detail", "Repository not synced yet. Use the API /sync endpoint first."))

            # Stored commits
            resp2 = requests.get(
                f"{API_BASE}/api/repos/{owner}/{repo}/commits/stored?page=1&limit=20",
                timeout=15
            )
            if resp2.status_code == 200:
                d2 = resp2.json()
                commits = d2.get("commits", [])
                if commits:
                    st.subheader(f"Recent Commits ({d2['total']} total)")
                    st.dataframe(
                        {
                            "SHA": [c["sha"] for c in commits],
                            "Author": [c["author"] for c in commits],
                            "Message": [c["message"] for c in commits],
                            "Date": [c["date"] for c in commits],
                        },
                        use_container_width=True,
                        hide_index=True,
                    )

        except Exception as e:
            st.error(f"Could not reach the API. Try again in 30 seconds.\n\n{e}")


# PAGE 4 — LOGIN / REGISTER

elif page == "Login":
    st.header("🔐 Authentication")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login to DevPulse")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", type="primary"):
            if username and password:
                try:
                    resp = requests.post(
                        f"{API_BASE}/api/auth/login",
                        data={"username": username, "password": password, "grant_type": "password"},
                        timeout=15
                    )
                    if resp.status_code == 200:
                        token = resp.json()["access_token"]
                        st.session_state["token"] = token
                        st.session_state["username"] = username
                        st.success(f"Logged in as {username}")
                        st.code(f"Token: {token[:40]}...", language=None)
                    else:
                        st.error("Incorrect username or password.")
                except Exception as e:
                    st.error(f"API error: {e}")
            else:
                st.warning("Please enter username and password.")

    with tab2:
        st.subheader("Create an Account")
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register", type="primary"):
            if new_user and new_pass:
                try:
                    resp = requests.post(
                        f"{API_BASE}/api/auth/register",
                        data={"username": new_user, "password": new_pass, "grant_type": "password"},
                        timeout=15
                    )
                    if resp.status_code == 200:
                        st.success(f"Account created for {new_user}. Go to Login tab.")
                    else:
                        st.error(resp.json().get("detail", "Registration failed."))
                except Exception as e:
                    st.error(f"API error: {e}")
            else:
                st.warning("Please fill in all fields.")