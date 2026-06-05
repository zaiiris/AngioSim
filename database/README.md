# Database

The first prototype uses SQLite.

Runtime file:

```text
database/angiosim.db
```

The FastAPI backend creates the database automatically on startup.

Current tables:

- `users`
- `training_sessions`
- `ai_results`
- `scores`

Later, this can move to PostgreSQL without changing the frontend flow.
