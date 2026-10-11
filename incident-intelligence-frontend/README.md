# Incident Intelligence Platform — frontend

React + Vite incident-response UI wired to the FastAPI endpoints visible in the supplied backend code.

## Run locally

```powershell
npm install
Copy-Item .env.example .env
npm run dev
```

Open the Vite URL shown in the terminal (usually `http://localhost:5173`). The API defaults to `http://localhost:8000`; override `VITE_API_BASE_URL` in `.env` if needed.

## Real product workflows

- Login: `POST /auth/login` (OAuth2 form data: `username` containing the account email, plus `password`, as used by the running router).
- Dashboard and queue: `GET /incidents`.
- Create incident: `POST /incidents`.
- View incident: `GET /incidents/{incident_id}`.
- Update incident: `PATCH /incidents/{incident_id}`.
- Incident timeline: `GET /incidents/{incident_id}/events` (verify the exact route and response in the running API).
- Stored AI analysis and history: `GET /incidents/{incident_id}/ai-analysis` and `GET /incidents/{incident_id}/ai-analysis/versions`.

The overview metrics, priority list, age warning, filters, sorting, and CSV export are derived from records returned by the API. CSV export is a client-side utility for the currently filtered set.

## Important boundaries

- API docs and Grafana/Prometheus links were removed from the product navigation; they are developer/operations tools, not core incident workflows.
- The UI does not show a fabricated activity chart or claim that all services are healthy.
- AI analysis is read-only in the UI. The backend currently persists/version-controls analysis payloads; actual ML inference is not confirmed in the provided code. The UI does not send a fake inference request.
- Assignment and comments are not presented as functional UI workflows because those routers were not registered in the supplied `app/main.py`.

## Build

```powershell
npm run build
```
