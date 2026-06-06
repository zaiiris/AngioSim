# AngioSim

AngioSim is a training platform for endovascular/surgical simulation.

Project parts:

- `frontend/` - user interface
- `backend/` - API that will connect frontend, AI, database, and hardware data
- `ai/` - model notebooks, datasets, and exported model files
- `hardware/` - Arduino trainer code and device notes
- `database/` - database schema, migrations, and seed data
- `docs/` - project documentation and architecture notes
- `infra/` - deployment and environment setup

## Run Locally

Start the backend in PowerShell window 1:

```powershell
.\start_backend.ps1
```

Start the frontend in PowerShell window 2:

```powershell
.\start_frontend.ps1
```

Open this address in your normal browser, for example Yandex Browser:

```text
http://127.0.0.1:8080/index.html
```

Keep both PowerShell windows open while you use the app. If you close them, the local site stops.

Backend API runs here:

```text
http://127.0.0.1:8000
```

Demo users:

```text
ziada@angiosim.local / demo
teacher@angiosim.local / demo
```

Optional API smoke check after the backend is running:

```powershell
.\smoke_check.ps1
```

## Current State

The project uses a static HTML/CSS frontend prototype in:

`frontend/static/`

Open `frontend/static/index.html` to view the first page.

## Future Flow

1. Arduino trainer sends sensor/action data.
2. Backend receives and stores that data.
3. AI model analyzes images/session data.
4. Frontend shows training, results, profile, leaderboard, and teacher views.
