# Backend

FastAPI server for AngioSim.

Current prototype:

- creates training sessions
- stores data in SQLite
- accepts suture image uploads
- runs YOLOv8 suture analysis when `ai/models/suture_yolov8_best.pt` exists
- falls back to deterministic mock analysis when YOLO dependencies are missing
- saves AI analysis results
- returns session history
- returns teacher monitoring data for students and group sessions

## Run locally

From the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000/api/health
```

Useful demo endpoints:

```text
http://localhost:8000/api/dashboard/summary
http://localhost:8000/api/teacher/students
http://localhost:8000/api/teacher/sessions
```

The first run creates:

```text
database/angiosim.db
backend/uploads/suture_images/
```

These local runtime files are ignored by git.

## AI model

Expected local model path:

```text
ai/models/suture_yolov8_best.pt
```

This file is ignored by git. If it exists and `ultralytics` is installed, `/api/ai/analyze-suture` uses the real YOLOv8 detector. Otherwise, the endpoint still works with mock analysis.
