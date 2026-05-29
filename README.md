# RetailQ
RetailIQ is a Python + SQL portfolio project for small retail businesses. It tracks products, sales, stock levels, and gives analytics such as monthly revenue, best-selling products, low-stock items, and stock risk forecasting.
This project is designed to show practical backend, SQL, and data skills for interviews.

## Features

- Product inventory database
- Customer and supplier tables
- Sales records
- Low-stock detection
- Revenue analytics
- Best-selling product report
- Stock risk forecast based on recent sales
- FastAPI backend
- Connected HTML/CSS/JavaScript frontend served by FastAPI
- Streamlit dashboard
- SQLite by default, PostgreSQL-ready through `RETAILIQ_DATABASE_URL`

## Tech Stack

- Python
- SQLAlchemy
- SQLite / PostgreSQL
- FastAPI
- Pandas
- Streamlit
- Pytest

## Setup

If `py` or `python` is not recognized, install Python 3.12 from the official Python website and enable "Add Python to PATH" during installation.

Create and activate a virtual environment:

```powershell
cd C:\Users\hstps\Music\RetailIQ
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

In this workspace, a `.venv` has already been created and dependencies have been installed.

Create sample data:

```powershell
python -m retailiq.seed --reset
```

Run the API:
Run the live web app:

```powershell
uvicorn retailiq.api.main:app --reload
```

Open the app:

```text
http://127.0.0.1:8000
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

Optional Streamlit dashboard:

```powershell
streamlit run retailiq/dashboard/app.py
```

## Useful API Endpoints

- `GET /health`
- `GET /products`
- `POST /products`
- `POST /sales`
- `GET /analytics/overview`
- `GET /analytics/revenue-by-month`
- `GET /analytics/top-products`
- `GET /analytics/low-stock`
- `GET /forecast/stock-risk`

## Interview Pitch

RetailIQ is a sales analytics and inventory forecasting platform for small retailers. I built a relational database, backend API, dashboard, and forecasting logic that estimates how soon products may run out based on recent sales velocity.

## Next Improvements

- Add login and role-based access
- Add CSV sales import
- Add PostgreSQL deployment
- Add product update/delete endpoints
- Add invoice generation
- Add Docker setup

