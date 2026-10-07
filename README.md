# Unit Management API

A FastAPI service for managing emergency response units (ambulances, fire trucks, police), backed by PostgreSQL.

## Run with Docker (recommended)

The quickest way to get running. Requires [Docker](https://docs.docker.com/get-docker/) with the Compose plugin; no local Python or PostgreSQL needed.

```bash
docker compose up --build
```

This starts two services:

- **`db`**: PostgreSQL 16 with the `unit_management` database (user/password `postgres`/`postgres`). Data is kept in the `pgdata` named volume.
- **`api`**: the FastAPI app. It waits for the database health check to pass, runs `alembic upgrade head`, then serves on port 8000.

Interactive docs are at http://localhost:8000/docs.

Useful commands:

```bash
docker compose up -d --build   # run in the background
docker compose logs -f api     # follow API logs
docker compose down            # stop containers (data is kept)
docker compose down -v         # stop and delete the database volume
```

The Compose setup sets its own `DATABASE_URL` and does not read `.env`. The credentials in `docker-compose.yml` are for local development only.

## Local setup (without Docker)

### Requirements

- Python 3.12+
- PostgreSQL

### Steps

1. **Create the database.** On Linux, as the `postgres` user:

   ```bash
   sudo -u postgres createdb unit_management
   ```

   Or from psql / pgAdmin:

   ```sql
   CREATE DATABASE unit_management;
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # Linux/macOS
   # .venv\Scripts\activate       # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment variables.** Copy `.env.example` to `.env` (`cp .env.example .env`) and fill in your PostgreSQL credentials:

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

## Running tests

The tests use an in-memory SQLite database, so they don't need PostgreSQL or Docker. With the virtual environment active:

```bash
pytest
```

## Endpoints

| Method | Path                           | Description                                     |
|--------|--------------------------------|-------------------------------------------------|
| GET    | `/api/units`                   | List units (filter by `status`, `unit_type`, `station_location`) |
| GET    | `/api/units/{unit_id}`         | Get one unit                                    |
| POST   | `/api/units`                   | Create a unit (callsign is generated)           |
| PATCH  | `/api/units/{unit_id}`         | Update `unit_type` and/or `station_location`    |
| PATCH  | `/api/units/{unit_id}/status`  | Update a unit's status                          |
| DELETE | `/api/units/{unit_id}`         | Delete a unit                                   |
