# GrantHunter AI - Walkthrough & Setup Guide

## 1. Prerequisites
- **Docker Desktop** installed and running.
- **Python 3.10+** installed.
- **Google Gemini API Key** (Get it from Google AI Studio).
- **Brave Search API Key** (Get it from Brave).

## 2. Setup

### Step 1: Configure Environment
1.  Rename `.env.example` to `.env` (if not already done).
2.  Open `.env` and paste your API keys:
    ```env
    GOOGLE_API_KEY=AIzaSy...
    BRAVE_SEARCH_API_KEY=BSA...
    ```

### Step 2: Start Infrastructure
Run the following command to start PostgreSQL and the Playwright Service:
```bash
docker-compose up -d
```

### Step 3: Install Dependencies
Create a virtual environment and install the requirements:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r backend/requirements.txt
```

## 3. Running the Application

### Option A: Run the Full App (Streamlit)
```bash
streamlit run frontend/app.py
```
- Open your browser at `http://localhost:8501`.
- Upload a Markdown file with your profile.
- Enter a query (e.g., "Becas de maestría en IA en España").
- Click "Launch Discovery Agent".

### Option B: Run Verification Scripts
To test individual components without the UI:

**Test Scraper (Playwright + Docker):**
```bash
python tests/verify_scraper.py
```

**Test Full Flow (End-to-End):**
```bash
python tests/verify_flow.py
```

## 4. Troubleshooting
- **Playwright Connection Refused**: Ensure the Docker container `granthunter_browser` is running (`docker ps`).
- **Database Error**: Ensure `granthunter_db` is running.
