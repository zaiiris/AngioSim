from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .ai_service import analysis_to_json, analyze_suture_image, save_upload
from .database import get_connection, init_db, row_to_dict, utc_now


app = FastAPI(title="AngioSim API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_user_summary(user_id: int = 1) -> dict:
    with get_connection() as conn:
        aggregate = conn.execute(
            """
            SELECT
                COUNT(sc.id) AS completed_sessions,
                COALESCE(ROUND(AVG(sc.total_score), 1), 0) AS average_score,
                COALESCE(MAX(sc.total_score), 0) AS best_score,
                COALESCE(ROUND(AVG(ar.uniformity_percent), 1), 0) AS average_uniformity
            FROM training_sessions s
            LEFT JOIN scores sc ON sc.session_id = s.id
            LEFT JOIN ai_results ar ON ar.id = (
                SELECT id FROM ai_results WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1
            )
            WHERE s.user_id = ?
            """,
            (user_id,),
        ).fetchone()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    completed = int(aggregate["completed_sessions"] or 0)
    average_score = float(aggregate["average_score"] or 0)
    best_score = int(aggregate["best_score"] or 0)
    average_uniformity = float(aggregate["average_uniformity"] or 0)
    achievements = min(12, max(0, best_score // 15 + completed // 5))
    xp = completed * 100 + best_score * 5

    return {
        "user": row_to_dict(user),
        "summary": {
            "completed_sessions": completed,
            "average_score": average_score,
            "best_score": best_score,
            "achievements": achievements,
            "average_uniformity": average_uniformity,
            "xp": xp,
            "next_level_xp": 1500,
        },
    }


def build_user_sessions(user_id: int = 1, limit: int = 25) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                s.id,
                s.mode,
                s.vessel_size,
                s.goal,
                s.started_at,
                s.ended_at,
                s.duration_seconds,
                s.notes,
                COALESCE(sc.total_score, 0) AS total_score,
                COALESCE(sc.leak_score, 0) AS leak_score,
                COALESCE(sc.pressure_score, 0) AS pressure_score,
                COALESCE(sc.speed_score, 0) AS speed_score,
                COALESCE(sc.ai_score, 0) AS ai_score,
                COALESCE(ar.osats_score, 0) AS osats_score,
                COALESCE(ar.stitch_count, 0) AS stitch_count,
                COALESCE(ar.uniformity_percent, 0) AS uniformity_percent,
                ar.feedback
            FROM training_sessions s
            LEFT JOIN scores sc ON sc.session_id = s.id
            LEFT JOIN ai_results ar ON ar.id = (
                SELECT id FROM ai_results WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1
            )
            WHERE s.user_id = ? AND (sc.id IS NOT NULL OR ar.id IS NOT NULL)
            ORDER BY s.started_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]


def level_for_score(score: float, sessions_count: int) -> str:
    if score >= 88 and sessions_count >= 10:
        return "Expert"
    if score >= 80:
        return "Advanced"
    if score >= 65:
        return "Intermediate"
    return "Beginner"


def initials_for_name(full_name: str) -> str:
    parts = [part for part in full_name.replace(".", " ").split() if part]
    return "".join(part[0] for part in parts[:2]).upper() or "AS"


def build_teacher_students() -> dict:
    with get_connection() as conn:
        rows = conn.execute(
            """
            WITH student_stats AS (
                SELECT
                    u.id,
                    u.full_name,
                    u.email,
                    u.university,
                    COUNT(sc.id) AS completed_sessions,
                    COALESCE(ROUND(AVG(sc.total_score), 1), 0) AS average_score,
                    COALESCE(MAX(sc.total_score), 0) AS best_score,
                    COALESCE(ROUND(AVG(ar.osats_score), 1), 0) AS average_osats,
                    COALESCE(ROUND(AVG(ar.uniformity_percent), 1), 0) AS average_uniformity,
                    MAX(s.started_at) AS last_session_at,
                    CAST(COALESCE(julianday('now') - julianday(MAX(s.started_at)), 999) AS INTEGER) AS inactive_days
                FROM users u
                LEFT JOIN training_sessions s ON s.user_id = u.id
                LEFT JOIN scores sc ON sc.session_id = s.id
                LEFT JOIN ai_results ar ON ar.id = (
                    SELECT id FROM ai_results WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1
                )
                WHERE u.role = 'student'
                GROUP BY u.id
            )
            SELECT * FROM student_stats
            ORDER BY average_score DESC, completed_sessions DESC, full_name ASC
            """
        ).fetchall()
        progress_rows = conn.execute(
            """
            SELECT
                strftime('%Y-%m', s.started_at) AS month,
                COALESCE(ROUND(AVG(sc.total_score), 1), 0) AS average_score,
                COALESCE(ROUND(AVG(ar.osats_score), 2), 0) AS average_osats,
                COUNT(sc.id) AS completed_sessions
            FROM training_sessions s
            JOIN scores sc ON sc.session_id = s.id
            LEFT JOIN ai_results ar ON ar.id = (
                SELECT id FROM ai_results WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1
            )
            GROUP BY strftime('%Y-%m', s.started_at)
            ORDER BY month DESC
            LIMIT 6
            """
        ).fetchall()

    students = []
    for row in rows:
        student = dict(row)
        student["initials"] = initials_for_name(student["full_name"])
        student["level"] = level_for_score(
            float(student["average_score"] or 0),
            int(student["completed_sessions"] or 0),
        )
        student["needs_attention"] = (
            int(student["completed_sessions"] or 0) == 0
            or int(student["inactive_days"] or 0) >= 10
            or float(student["average_score"] or 0) < 60
            or float(student["average_osats"] or 0) < 2.5
        )
        if int(student["completed_sessions"] or 0) == 0:
            student["attention_reason"] = "No completed sessions yet"
        elif int(student["inactive_days"] or 0) >= 10:
            student["attention_reason"] = f"No activity for {student['inactive_days']} days"
        elif float(student["average_osats"] or 0) < 2.5:
            student["attention_reason"] = "OSATS below 2.5"
        elif float(student["average_score"] or 0) < 60:
            student["attention_reason"] = "Average score below 60"
        else:
            student["attention_reason"] = ""
        students.append(student)

    completed_total = sum(int(student["completed_sessions"] or 0) for student in students)
    averages = [float(student["average_score"] or 0) for student in students if student["completed_sessions"]]
    attention = [student for student in students if student["needs_attention"]]

    return {
        "summary": {
            "students_count": len(students),
            "completed_sessions": completed_total,
            "average_score": round(sum(averages) / len(averages), 1) if averages else 0,
            "attention_count": len(attention),
        },
        "students": students,
        "attention": attention,
        "group_progress": [dict(row) for row in reversed(progress_rows)],
    }


def build_teacher_sessions(limit: int = 50) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                s.id,
                s.user_id,
                u.full_name AS student_name,
                u.university,
                s.mode,
                s.vessel_size,
                s.goal,
                s.started_at,
                s.ended_at,
                s.duration_seconds,
                COALESCE(sc.total_score, 0) AS total_score,
                COALESCE(sc.leak_score, 0) AS leak_score,
                COALESCE(sc.pressure_score, 0) AS pressure_score,
                COALESCE(sc.speed_score, 0) AS speed_score,
                COALESCE(sc.ai_score, 0) AS ai_score,
                COALESCE(ar.osats_score, 0) AS osats_score,
                COALESCE(ar.stitch_count, 0) AS stitch_count,
                COALESCE(ar.uniformity_percent, 0) AS uniformity_percent,
                ar.feedback
            FROM training_sessions s
            JOIN users u ON u.id = s.user_id
            LEFT JOIN scores sc ON sc.session_id = s.id
            LEFT JOIN ai_results ar ON ar.id = (
                SELECT id FROM ai_results WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1
            )
            WHERE u.role = 'student'
            ORDER BY s.started_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def build_ai_recommendation(summary: dict) -> str:
    completed = int(summary["completed_sessions"] or 0)
    average_score = float(summary["average_score"] or 0)
    average_uniformity = float(summary["average_uniformity"] or 0)

    if completed == 0:
        return "Start your first session and upload a suture photo to unlock AI recommendations."
    if average_uniformity and average_uniformity < 80:
        return (
            f"Main focus: stitch uniformity is averaging {average_uniformity:.0f}%. "
            "Run 2-3 Ordinary 6mm sessions and focus on equal spacing before increasing speed."
        )
    if average_score < 75:
        return (
            f"Average score is {average_score:.1f}. Keep sessions slower and prioritize stable needle angle and spacing."
        )
    return (
        "Progress is stable. Continue with mixed Ordinary and Adrenalin sessions to keep quality under pressure."
    )


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/sessions")
def create_session(payload: dict) -> dict:
    user_id = int(payload.get("user_id") or 1)
    mode = str(payload.get("mode") or "ord")
    vessel_size = str(payload.get("vessel_size") or "6mm")
    goal = str(payload.get("goal") or "tech")

    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO training_sessions (user_id, mode, vessel_size, goal, started_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, mode, vessel_size, goal, utc_now()),
        )
        session_id = cur.lastrowid
        row = conn.execute(
            "SELECT * FROM training_sessions WHERE id = ?", (session_id,)
        ).fetchone()

    return {"session": row_to_dict(row)}


@app.get("/api/sessions")
def list_sessions() -> dict:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                s.*,
                ar.osats_score,
                ar.stitch_count,
                ar.uniformity_percent,
                sc.total_score
            FROM training_sessions s
            LEFT JOIN ai_results ar ON ar.id = (
                SELECT id FROM ai_results WHERE session_id = s.id ORDER BY created_at DESC LIMIT 1
            )
            LEFT JOIN scores sc ON sc.session_id = s.id
            ORDER BY s.started_at DESC
            LIMIT 25
            """
        ).fetchall()
    return {"sessions": [dict(row) for row in rows]}


@app.get("/api/sessions/{session_id}")
def get_session(session_id: int) -> dict:
    with get_connection() as conn:
        session = conn.execute(
            "SELECT * FROM training_sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        ai_result = conn.execute(
            "SELECT * FROM ai_results WHERE session_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        ).fetchone()
        score = conn.execute(
            "SELECT * FROM scores WHERE session_id = ?", (session_id,)
        ).fetchone()
    return {
        "session": row_to_dict(session),
        "ai_result": row_to_dict(ai_result),
        "score": row_to_dict(score),
    }


@app.get("/api/results/latest")
def get_latest_result() -> dict:
    with get_connection() as conn:
        session = conn.execute(
            """
            SELECT s.*
            FROM training_sessions s
            LEFT JOIN ai_results ar ON ar.session_id = s.id
            LEFT JOIN scores sc ON sc.session_id = s.id
            WHERE ar.id IS NOT NULL OR sc.id IS NOT NULL
            ORDER BY started_at DESC
            LIMIT 1
            """
        ).fetchone()
        if session is None:
            raise HTTPException(status_code=404, detail="No saved results found")

        session_id = session["id"]
        ai_result = conn.execute(
            "SELECT * FROM ai_results WHERE session_id = ? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        ).fetchone()
        score = conn.execute(
            "SELECT * FROM scores WHERE session_id = ?", (session_id,)
        ).fetchone()
        history = conn.execute(
            """
            SELECT s.id, s.started_at, COALESCE(sc.total_score, 0) AS total_score
            FROM training_sessions s
            LEFT JOIN scores sc ON sc.session_id = s.id
            ORDER BY s.started_at DESC
            LIMIT 6
            """
        ).fetchall()

    return {
        "session": row_to_dict(session),
        "ai_result": row_to_dict(ai_result),
        "score": row_to_dict(score),
        "history": [dict(row) for row in reversed(history)],
    }


@app.get("/api/dashboard/summary")
def get_dashboard_summary(user_id: int = 1) -> dict:
    profile = build_user_summary(user_id)
    recent_sessions = build_user_sessions(user_id, limit=6)
    with get_connection() as conn:
        progress = conn.execute(
            """
            SELECT s.id, s.started_at, COALESCE(sc.total_score, 0) AS total_score
            FROM training_sessions s
            JOIN scores sc ON sc.session_id = s.id
            WHERE s.user_id = ?
            ORDER BY s.started_at DESC
            LIMIT 12
            """,
            (user_id,),
        ).fetchall()

    progress_rows = [dict(row) for row in reversed(progress)]

    return {
        "summary": profile["summary"],
        "recommendation": build_ai_recommendation(profile["summary"]),
        "recent_sessions": recent_sessions,
        "progress": progress_rows,
    }


@app.get("/api/teacher/students")
def get_teacher_students() -> dict:
    return build_teacher_students()


@app.get("/api/teacher/sessions")
def get_teacher_sessions(limit: int = 50) -> dict:
    return {"sessions": build_teacher_sessions(limit=limit)}


@app.get("/api/users/{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    profile = build_user_summary(user_id)
    sessions = build_user_sessions(user_id, limit=5)
    summary = profile["summary"]

    skills = {
        "suture_quality": int(summary["average_score"] or 0),
        "speed": int(sum(row["speed_score"] for row in sessions) / len(sessions)) if sessions else 0,
        "pressure": int(sum(row["pressure_score"] for row in sessions) / len(sessions)) if sessions else 0,
        "leak_control": int(sum(row["leak_score"] for row in sessions) / len(sessions)) if sessions else 0,
        "uniformity": int(summary["average_uniformity"] or 0),
    }
    achievements = [
        {"name": "First suture", "unlocked": summary["completed_sessions"] >= 1},
        {"name": "Good result", "unlocked": summary["best_score"] >= 80},
        {"name": "AI evaluator", "unlocked": summary["best_score"] >= 90},
        {"name": "Consistent practice", "unlocked": summary["completed_sessions"] >= 5},
        {"name": "Expert", "unlocked": summary["xp"] >= summary["next_level_xp"]},
    ]

    return {
        **profile,
        "skills": skills,
        "achievements": achievements,
        "recent_sessions": sessions,
    }


@app.get("/api/users/{user_id}/sessions")
def get_user_sessions(user_id: int, limit: int = 25) -> dict:
    return {"sessions": build_user_sessions(user_id, limit=limit)}


@app.post("/api/ai/analyze-suture")
async def analyze_suture(
    session_id: Annotated[int, Form()],
    image: Annotated[UploadFile, File()],
) -> dict:
    content = await image.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty image upload")

    image_path = save_upload(session_id, image.filename or "suture.jpg", content)
    analysis = analyze_suture_image(image_path)
    ai_score = round(analysis.osats_score / 5 * 100)
    total_score = round(ai_score * 0.55 + analysis.uniformity_percent * 0.25 + 85 * 0.20)

    with get_connection() as conn:
        session = conn.execute(
            "SELECT id FROM training_sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        cur = conn.execute(
            """
            INSERT INTO ai_results (
                session_id, image_path, osats_score, stitch_count, uniformity_percent,
                confidence, feedback, raw_predictions_json, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                str(image_path),
                analysis.osats_score,
                analysis.stitch_count,
                analysis.uniformity_percent,
                analysis.confidence,
                analysis.feedback,
                analysis_to_json(analysis),
                utc_now(),
            ),
        )
        conn.execute(
            """
            INSERT INTO scores (
                session_id, total_score, leak_score, pressure_score, speed_score, ai_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                total_score = excluded.total_score,
                ai_score = excluded.ai_score,
                created_at = excluded.created_at
            """,
            (session_id, total_score, 85, 85, 82, ai_score, utc_now()),
        )
        result_id = cur.lastrowid

    return {
        "id": result_id,
        "session_id": session_id,
        "osats_score": analysis.osats_score,
        "stitch_count": analysis.stitch_count,
        "uniformity_percent": analysis.uniformity_percent,
        "confidence": analysis.confidence,
        "feedback": analysis.feedback,
        "total_score": total_score,
        "raw_predictions": analysis.raw_predictions,
    }


@app.post("/api/sessions/{session_id}/finish")
def finish_session(session_id: int, payload: dict) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM training_sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Session not found")
        conn.execute(
            """
            UPDATE training_sessions
            SET ended_at = ?, duration_seconds = ?, notes = ?
            WHERE id = ?
            """,
            (
                utc_now(),
                int(payload.get("duration_seconds") or 0),
                str(payload.get("notes") or ""),
                session_id,
            ),
        )
        updated = conn.execute(
            "SELECT * FROM training_sessions WHERE id = ?", (session_id,)
        ).fetchone()

    return {"session": row_to_dict(updated)}
