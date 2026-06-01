# Health Monitor System

A web-based health monitoring application built with Flask, MySQL, and Docker.

## Project Structure

```
health_monitor/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   └── routes/
│       ├── auth.py          # Login / Register
│       ├── patient.py       # Patient dashboard & readings
│       ├── doctor.py        # Doctor views & notes
│       └── admin.py         # Admin management
├── static/
│   ├── css/style.css
│   └── js/main.js
├── templates/               # HTML pages
├── tests/test_app.py        # Pytest tests
├── config.py
├── run.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Setup (Local with Anaconda)

```bash
# 1. Activate your conda environment
conda activate health_monitor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up MySQL database
#    Open MySQL and run:
#    CREATE DATABASE health_monitor;

# 4. Update config.py with your MySQL password

# 5. Run the app
python run.py
```

Visit: http://localhost:5000

## Setup (Docker)

```bash
docker-compose up --build
```

Visit: http://localhost:5000

## Running Tests

```bash
pytest tests/ -v
```

## User Roles

| Role    | Access                                      |
|---------|---------------------------------------------|
| Patient | Add readings, view dashboard & history      |
| Doctor  | View assigned patients, add notes           |
| Admin   | Manage users, assign patients to doctors    |
