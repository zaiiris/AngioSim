# Database

The first prototype uses SQLite.

Runtime file:

```text
database/angiosim.db
```

The FastAPI backend creates the database automatically on startup.

The source schema is kept in:

```text
database/schema.sql
```

Current tables:

- `users`
- `lessons`
- `achievements`
- `training_sessions`
- `ai_results`
- `scores`
- `session_events`
- `hardware_events`

Demo seed data is inserted idempotently by `backend/app/database.py`, so the app can be run from a fresh checkout and immediately show dashboard, results, and teacher monitoring views.

Later, this can move to PostgreSQL without changing the frontend flow.
