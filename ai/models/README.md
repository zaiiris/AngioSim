# AI Models

Put exported model files here during local development.

Expected YOLOv8 file:

```text
suture_yolov8_best.pt
```

Model weights are ignored by git because they are usually large binary files.

## Where to store the model

For the MVP, keep the trained model in Google Drive and copy it into this folder for local runs.

Expected local path:

```text
ai/models/suture_yolov8_best.pt
```

Recommended Drive file name:

```text
suture_yolov8_best.pt
```

After downloading the file, verify it from the project root:

```powershell
backend\.venv\Scripts\python.exe -c "from backend.app.ai_service import MODEL_PATH; print(MODEL_PATH.exists(), MODEL_PATH)"
```

Git LFS can be added later when the model needs strict versioning inside GitHub. Until then, `.pt` files stay ignored by git.
