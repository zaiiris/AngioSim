from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
DATABASE_DIR = ROOT_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "angiosim.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


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
        try:
            conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
            seed_demo_data(conn)
        except sqlite3.OperationalError as exc:
            if "readonly database" not in str(exc):
                raise


def seed_demo_data(conn: sqlite3.Connection) -> None:
    now = utc_now()
    users = [
        (1, "Demo Student", "student@angiosim.local", "student", "AngioSim Demo"),
        (2, "Aigerim A.", "aigerim@angiosim.local", "student", "NIS EMN Turkestan"),
        (3, "Ziada A.", "ziada@angiosim.local", "student", "NIS EMN Turkestan"),
        (4, "Daniyar M.", "daniyar@angiosim.local", "student", "NIS EMN Turkestan"),
        (5, "Erlan K.", "erlan@angiosim.local", "student", "NIS EMN Turkestan"),
        (6, "Bolat T.", "bolat@angiosim.local", "student", "NIS EMN Turkestan"),
        (7, "Madina S.", "madina@angiosim.local", "student", "NIS EMN Turkestan"),
        (100, "Lipakova I.N.", "teacher@angiosim.local", "teacher", "NIS EMN Turkestan"),
    ]
    conn.executemany(
        """
        INSERT OR IGNORE INTO users (id, full_name, email, role, university, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [(user_id, name, email, role, university, now) for user_id, name, email, role, university in users],
    )

    lessons = [
        (1, "Vascular Anatomy", "basics", "Basic artery and vein structure", 18, "beginner"),
        (2, "Anastomosis Technique", "technique", "Step-by-step vascular suture guide", 34, "intermediate"),
        (3, "Hemodynamics", "theory", "Pressure, flow, and clinical norms", 22, "intermediate"),
        (4, "AI Suture Assessment", "ai", "How to read AngioSim AI results", 15, "beginner"),
    ]
    conn.executemany(
        """
        INSERT OR IGNORE INTO lessons (id, title, category, description, duration_minutes, level, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [(lesson_id, title, category, description, duration, level, now) for lesson_id, title, category, description, duration, level in lessons],
    )

    achievements = [
        (1, "First suture", "Complete the first training session", "first_session"),
        (2, "Good result", "Score 80 or higher", "score_80"),
        (3, "AI evaluator", "Upload a suture image for AI assessment", "ai_upload"),
        (4, "Consistent practice", "Complete five sessions", "five_sessions"),
        (5, "Expert", "Reach 1500 XP", "xp_1500"),
    ]
    conn.executemany(
        """
        INSERT OR IGNORE INTO achievements (id, name, description, code, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        [(achievement_id, name, description, code, now) for achievement_id, name, description, code in achievements],
    )

    demo_sessions = [
        (1, 1, "ord", "6mm", "tech", "2026-05-01T09:00:00+00:00", "2026-05-01T09:05:10+00:00", 310, 76, 3.8, 8, 82),
        (2, 1, "ord", "6mm", "tech", "2026-05-10T10:10:00+00:00", "2026-05-10T10:14:20+00:00", 260, 84, 4.1, 9, 86),
        (101, 2, "adr", "4mm", "speed", "2026-05-23T08:30:00+00:00", "2026-05-23T08:33:55+00:00", 235, 91, 4.6, 10, 91),
        (102, 2, "ord", "6mm", "tech", "2026-06-02T12:10:00+00:00", "2026-06-02T12:14:08+00:00", 248, 88, 4.4, 9, 89),
        (103, 3, "ord", "6mm", "tech", "2026-05-26T11:20:00+00:00", "2026-05-26T11:24:30+00:00", 270, 79, 3.9, 8, 81),
        (104, 3, "adr", "4mm", "speed", "2026-06-03T13:40:00+00:00", "2026-06-03T13:44:12+00:00", 252, 83, 4.2, 9, 84),
        (105, 4, "ord", "6mm", "tech", "2026-05-28T09:45:00+00:00", "2026-05-28T09:49:50+00:00", 290, 85, 4.3, 9, 86),
        (106, 5, "ord", "10mm", "pressure", "2026-05-27T14:10:00+00:00", "2026-05-27T14:15:36+00:00", 336, 79, 3.8, 7, 77),
        (107, 5, "adr", "6mm", "speed", "2026-06-01T15:20:00+00:00", "2026-06-01T15:24:05+00:00", 245, 82, 4.0, 8, 80),
        (108, 6, "ord", "10mm", "tech", "2026-05-17T16:00:00+00:00", "2026-05-17T16:06:20+00:00", 380, 42, 2.1, 5, 52),
        (109, 7, "ord", "6mm", "tech", "2026-05-30T10:55:00+00:00", "2026-05-30T10:59:42+00:00", 282, 75, 3.6, 8, 78),
    ]
    conn.executemany(
        """
        INSERT OR IGNORE INTO training_sessions (
            id, user_id, mode, vessel_size, goal, started_at, ended_at, duration_seconds, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Demo seeded session')
        """,
        [(session_id, user_id, mode, vessel, goal, started, ended, duration) for session_id, user_id, mode, vessel, goal, started, ended, duration, *_ in demo_sessions],
    )

    conn.executemany(
        """
        INSERT OR IGNORE INTO scores (
            session_id, total_score, leak_score, pressure_score, speed_score, ai_score, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (session_id, total, min(98, total + 5), min(96, total + 1), min(96, total - 2), round(osats / 5 * 100), ended)
            for session_id, _user_id, _mode, _vessel, _goal, _started, ended, _duration, total, osats, _stitches, _uniformity in demo_sessions
        ],
    )

    conn.executemany(
        """
        INSERT OR IGNORE INTO ai_results (
            session_id, image_path, osats_score, stitch_count, uniformity_percent,
            confidence, feedback, raw_predictions_json, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                session_id,
                f"uploads/demo/session_{session_id}.jpg",
                osats,
                stitches,
                uniformity,
                0.86,
                "Demo AI feedback: keep stitch spacing even and control tension.",
                json.dumps({"metrics": {"gaps": [], "seeded": True}}),
                ended,
            )
            for session_id, _user_id, _mode, _vessel, _goal, _started, ended, _duration, _total, osats, stitches, uniformity in demo_sessions
        ],
    )

    conn.executemany(
        """
        INSERT OR IGNORE INTO session_events (session_id, event_type, value_json, created_at)
        VALUES (?, ?, ?, ?)
        """,
        [
            (session_id, "session_completed", json.dumps({"duration_seconds": duration}), ended)
            for session_id, _user_id, _mode, _vessel, _goal, _started, ended, duration, *_ in demo_sessions
        ],
    )

    conn.executemany(
        """
        INSERT OR IGNORE INTO hardware_events (session_id, sensor_name, value, unit, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (session_id, "pressure", 48 + (session_id % 9), "mmHg", ended)
            for session_id, _user_id, _mode, _vessel, _goal, _started, ended, *_ in demo_sessions
        ],
    )


def row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    data = dict(row)
    if "raw_predictions_json" in data:
        data["raw_predictions"] = json.loads(data.pop("raw_predictions_json"))
    return data
