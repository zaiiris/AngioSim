CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'student',
    university TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    duration_minutes INTEGER NOT NULL DEFAULT 0,
    level TEXT NOT NULL DEFAULT 'beginner',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    code TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS training_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    mode TEXT NOT NULL,
    vessel_size TEXT NOT NULL,
    goal TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    duration_seconds INTEGER,
    notes TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ai_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    osats_score REAL NOT NULL,
    stitch_count INTEGER NOT NULL,
    uniformity_percent INTEGER NOT NULL,
    confidence REAL NOT NULL,
    feedback TEXT NOT NULL,
    raw_predictions_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES training_sessions(id)
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL UNIQUE,
    total_score INTEGER NOT NULL,
    leak_score INTEGER NOT NULL,
    pressure_score INTEGER NOT NULL,
    speed_score INTEGER NOT NULL,
    ai_score INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES training_sessions(id)
);

CREATE TABLE IF NOT EXISTS session_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    value_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES training_sessions(id)
);

CREATE TABLE IF NOT EXISTS hardware_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    sensor_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES training_sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_training_sessions_user_started
    ON training_sessions(user_id, started_at);

CREATE INDEX IF NOT EXISTS idx_ai_results_session_created
    ON ai_results(session_id, created_at);

CREATE INDEX IF NOT EXISTS idx_scores_session
    ON scores(session_id);

CREATE INDEX IF NOT EXISTS idx_session_events_session
    ON session_events(session_id);

CREATE INDEX IF NOT EXISTS idx_hardware_events_session
    ON hardware_events(session_id);
