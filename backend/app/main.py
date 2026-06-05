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
