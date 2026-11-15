# Incident Intelligence Platform

An incident management workspace for recording service issues, tracking
their progress, coordinating ownership, and keeping investigation notes
in one place.

The project combines a FastAPI backend, a React frontend, PostgreSQL for
persistent data, Redis for caching, and Prometheus/Grafana for
application monitoring. It also includes an experimental root-cause
ranking component that works with supplied telemetry signals.

## What it does

-   Create and browse incidents with a service name, description,
    severity, and status.
-   View incident details and update severity, status, and the recorded
    cause.
-   Track status changes through an incident event timeline.
-   Assign users to incidents and manage active assignments.
-   Add comments for investigation notes and hand-offs.
-   Store analysis results against an incident and keep version history.
-   Apply JWT authentication and role-based access checks.
-   Cache incident-list responses in Redis while keeping PostgreSQL as
    the source of truth.
-   Expose application metrics for Prometheus and visualize them in
    Grafana.

## Tech stack

  -----------------------------------------------------------------------
  Area                                Technologies
  ----------------------------------- -----------------------------------
  Backend                             Python, FastAPI, Pydantic

  Database                            PostgreSQL, SQLAlchemy 2.x, Alembic

  Authentication                      JWT, Argon2 password hashing,
                                      role-based access control

  Caching                             Redis

  Frontend                            React, Vite, React Router, Axios

  Monitoring                          Prometheus, Grafana

  Containers                          Docker, Docker Compose

  RCA experimentation                 Python, Pandas, scikit-learn,
                                      RCAEval dataset
  -----------------------------------------------------------------------

## Architecture

``` mermaid
flowchart LR
    U[User] --> FE[React frontend]
    FE -->|HTTP / JSON| API[FastAPI]
    API --> AUTH[Authentication and permissions]
    API --> SVC[Feature services]
    SVC --> DB[(PostgreSQL)]
    SVC <--> R[(Redis cache)]
    API --> METRICS[/metrics endpoint/]
    PROM[Prometheus] -->|scrapes| METRICS
    GRAF[Grafana] --> PROM
```

The frontend sends HTTP requests to FastAPI. The backend validates
requests, applies authentication and permission checks, runs the
relevant feature logic, and uses SQLAlchemy to access PostgreSQL. Redis
is an optional cache layer; PostgreSQL remains the persistent source of
truth.

Prometheus scrapes the API's `/metrics` endpoint, and Grafana can use
Prometheus as its data source.

## Project structure

### Backend

The backend is organised by feature, with shared infrastructure under
`app/core/`.

-   `app/core/` --- settings, database sessions, JWT authentication,
    password hashing, permissions, Redis client, and metrics.
-   `app/features/Incident/` --- incident models, schemas, CRUD
    operations, services, and routes.
-   `app/features/Incident_Assignee/` --- incident assignment
    operations.
-   `app/features/Incident_Events/` --- incident event history.
-   `app/features/comments/` --- incident comments.
-   `app/features/users/`, `roles/`, and `user_roles/` --- user and role
    management.
-   `app/features/ai_analysis/` --- analysis records, version history,
    and RCA-related modules.
-   `app/scripts/create_admin.py` --- interactive initial administrator
    setup.
-   `app/main.py` --- creates the FastAPI application, registers
    routers, enables CORS, and exposes Prometheus metrics.

### Frontend

-   `src/pages/` --- login, dashboard, incident list, and incident
    detail screens.
-   `src/components/` --- reusable UI components such as badges and
    modals.
-   `src/layouts/` --- application layout.
-   `src/api/` --- Axios client and API functions for authentication,
    incidents, users, and analysis.
-   `src/App.jsx` and `src/main.jsx` --- application routes and React
    entry point.

## Root-cause analysis: current scope

The repository contains a notebook for experimentation and a Python
scoring implementation under `app/features/ai_analysis/rca/`.

The current backend scorer (`RCAEval-V1-rule-based`) is deterministic.
It ranks services using within-case percentile ranks of four supplied
early-change signals:

-   CPU
-   Memory
-   p50 latency
-   p90 latency

The inference helper validates telemetry records, builds a DataFrame,
runs the scorer, and formats a structured result containing ranked
candidate services and signal-level evidence.

**Important:** the current inference helper expects precomputed
early-change values. It does not collect live production telemetry or
calculate those early-change signals itself. The highest-ranked service
is an investigation candidate, not proof of a causal root cause. Scores
are ranking signals, not calibrated probabilities. Notebook experiments
and the backend's frozen V1 scorer are separate parts of the project;
notebook results should not be interpreted as proof that a trained model
is being served by the API.

## Run locally

### Prerequisites

-   Python compatible with the project dependencies
-   [uv](https://docs.astral.sh/uv/) for Python dependency management
-   Node.js and npm
-   A PostgreSQL database
-   Docker Desktop, if you want Redis and monitoring through Docker
    Compose

### 1. Configure the backend

Create a `.env` file in the backend root (the directory containing
`Dockerfile` and `docker-compose.yml`).

The backend settings expect:

``` env
user=YOUR_DATABASE_USER
password=YOUR_DATABASE_PASSWORD
host=YOUR_DATABASE_HOST
port=5432
dbname=YOUR_DATABASE_NAME

JWT_SECRET_KEY=REPLACE_WITH_A_LONG_RANDOM_SECRET
JWT_ALGORITHM=HS256
EXPIRATION=30
```

The database connection uses `sslmode=require`. Keep real credentials
and secrets out of Git. Commit an `.env.example` with placeholders
instead of committing `.env`.

### 2. Apply database migrations

From the backend root:

``` bash
uv sync
uv run alembic upgrade head
```

### 3. Create the initial administrator

After migrations have created the required tables and roles, run:

``` bash
uv run python -m app.scripts.create_admin
```

Follow the prompts for the administrator name, email, and password.
Password input is hidden in the terminal.

### 4. Start the backend

From the backend root:

``` bash
uv run uvicorn app.main:app --reload
```

The API is available at:

-   API: `http://localhost:8000`
-   Interactive API docs: `http://localhost:8000/docs`
-   Metrics: `http://localhost:8000/metrics`

For the Redis-backed read path, make sure Redis is running and
`REDIS_HOST` / `REDIS_PORT` point to it. When running the API directly
on your machine, the usual local values are `localhost` and `6379`.

### 5. Start the frontend

Open another terminal and move into the frontend directory:

``` bash
cd incident-intelligence-frontend
npm install
npm run dev
```

Vite normally serves the frontend at `http://localhost:5173`.

The frontend API client defaults to `http://localhost:8000`. To use a
different API address, create a frontend `.env` file:

``` env
VITE_API_BASE_URL=http://localhost:8000
```

## Run supporting services with Docker Compose

The supplied `docker-compose.yml` starts the API, Redis, Prometheus, and
Grafana. It does **not** build or start the React frontend; run the
frontend separately using the steps above.

From the backend root:

``` bash
docker compose up -d --build
docker compose ps
```

Useful URLs:

  Service                             Local address
  ----------------------------------- ------------------------------
  FastAPI                             `http://localhost:8000`
  FastAPI docs                        `http://localhost:8000/docs`
  Prometheus                          `http://localhost:9091`
  Grafana                             `http://localhost:3001`
  React / Vite (started separately)   `http://localhost:5173`

Useful commands:

``` bash
# Follow API logs
docker compose logs -f api

# View service status
docker compose ps

# Stop containers (keeps named volumes)
docker compose down
```

Redis uses a named Docker volume (`redis_data`) and starts with
append-only persistence enabled. Avoid `docker compose down -v` unless
you intentionally want to remove named volumes too.

The API container receives `REDIS_HOST=redis` and `REDIS_PORT=6379`,
because Compose services communicate using service names. Prometheus
scrapes the API at `api:8000/metrics` every 15 seconds.

## Redis caching notes

The incident-list cache key includes the requested page, page size,
status, severity, service filter, and a cache-version value. After
relevant writes, the version is incremented so later list requests use a
new cache key. Individual incident cache entries can also be
invalidated.

Redis reduces repeated reads; it is not the system of record. PostgreSQL
remains the persistent source of truth. Redis errors are tracked with
application counters, and the incident-list read path is designed to
fall back to PostgreSQL when Redis is unavailable.

## Monitoring

The API exposes Prometheus metrics through the FastAPI Prometheus
Instrumentator. The supplied `prometheus.yml` configures two scrape
targets:

-   Prometheus itself at `localhost:9090` from inside the Prometheus
    container.
-   The API at `api:8000/metrics` from the Prometheus container.

Grafana is available on port `3001` and can use the Prometheus service
as its data source. Dashboards and alert rules can be configured
separately.

## Security and configuration notes

-   Passwords are hashed with Argon2; raw passwords should not be
    stored.
-   Protected API routes use JWT bearer authentication.
-   Role checks are used for administrator-only and user-scoped
    operations.
-   Database credentials and the JWT signing secret belong in
    environment variables, not source control.
-   The CORS allow-list in `app/main.py` is configured for local
    development origins. Update it deliberately when deploying the
    frontend elsewhere.
-   The supplied Compose file is a development-oriented setup, not a
    complete production deployment configuration. Production use needs
    suitable secret management, network restrictions, TLS, backups,
    resource limits, and operational alerting.

## Current limitations

-   RCA input consists of precomputed telemetry signals; live telemetry
    ingestion and early-change feature calculation are outside the
    current inference helper.
-   The RCA V1 result is a ranked lead for investigation, not a
    confirmed cause or probability.
-   The supplied Compose file does not include a frontend service.
-   Prometheus scraping is configured, but Grafana dashboards and alert
    policies may need to be created separately.
-   Cloud hosting and an automated CI/CD pipeline are not included in
    the supplied project configuration.

## Possible next steps

-   Add a telemetry ingestion path and calculate early-change features
    from source metrics.
-   Evaluate and calibrate RCA ranking on clearly separated validation
    data before using it for operational decisions.
-   Add automated backend and frontend tests to a GitHub Actions
    workflow.
-   Add a production deployment configuration with managed secrets, TLS,
    backups, and health checks.
-   Add documented Grafana dashboards and alert rules.

## License

Add a license file before distributing or reusing this project publicly.
