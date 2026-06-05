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

## Current State

Right now the project contains the static HTML/CSS frontend prototype in:

`frontend/static/`

Open `frontend/static/index.html` to view the first page.

## Future Flow

1. Arduino trainer sends sensor/action data.
2. Backend receives and stores that data.
3. AI model analyzes images/session data.
4. Frontend shows training, results, profile, leaderboard, and teacher views.
