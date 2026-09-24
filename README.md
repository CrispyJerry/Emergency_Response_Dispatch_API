# Unit Management API

A FastAPI service for managing emergency response units (ambulances, fire trucks, police), backed by PostgreSQL.

## Requirements

- Python 3.12+
- PostgreSQL

## Setup

1. **Create the database** (in psql or pgAdmin):

   ```sql
   CREATE DATABASE unit_management;
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   ```

3. **Configure environment variables.** Copy `.env.example` to `.env` and fill in your PostgreSQL credentials:

   ```
   DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/unit_management
   ```

   The `postgresql+psycopg://` prefix is required because the project uses psycopg 3. `.env` is git-ignored, so never commit real credentials.

4. **Create the tables** with Alembic:

   ```bash
   alembic upgrade head
   ```

5. **Run the API:**

   ```bash
   uvicorn app.main:app --reload
   ```

   Interactive docs are at http://127.0.0.1:8000/docs.

## Endpoints

| Method | Path                           | Description                                     |
|--------|--------------------------------|-------------------------------------------------|
| GET    | `/api/units`                   | List units (filter by `status`, `unit_type`, `station_location`) |
| GET    | `/api/units/{unit_id}`         | Get one unit                                    |
| POST   | `/api/units`                   | Create a unit (callsign is generated)           |
| PATCH  | `/api/units/{unit_id}`         | Update `unit_type` and/or `station_location`    |
| PATCH  | `/api/units/{unit_id}/status`  | Update a unit's status                          |
| DELETE | `/api/units/{unit_id}`         | Delete a unit                                   |
