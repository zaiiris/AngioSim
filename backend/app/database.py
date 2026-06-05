from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
DATABASE_DIR = ROOT_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "angiosim.db"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection() -> sqlite3.Connection:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'student',
                university TEXT,
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
            """
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO users (id, full_name, email, role, university, created_at)
            VALUES (1, 'Demo Student', 'student@angiosim.local', 'student', 'AngioSim Demo', ?)
            """,
            (utc_now(),),
        )


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    data = dict(row)
    if "raw_predictions_json" in data:
        data["raw_predictions"] = json.loads(data.pop("raw_predictions_json"))
    return data
