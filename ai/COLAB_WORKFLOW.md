# AngioSim Colab Workflow

Use this when working with `ai_angiosim.ipynb` in Google Colab.

## Why files disappear

Colab runtime is temporary. Files uploaded through the left panel or `files.upload()` can disappear after runtime reset.

Keep important files in Google Drive:

- Roboflow dataset zip
- extracted dataset folder
- trained YOLO weights
- training logs and metrics

## Recommended Drive structure

Create this in Google Drive:

```text
MyDrive/AngioSimAI/
  datasets/
    roboflow_suture_dataset.zip
    roboflow_suture_dataset/
  models/
    suture_yolov8_best.pt
  runs/
  notebooks/
    ai_angiosim.ipynb
```

## Cell 1: connect Google Drive

Put this near the top of `ai_angiosim.ipynb`:

```python
from google.colab import drive
drive.mount("/content/drive")
```

## Cell 2: define paths

```python
from pathlib import Path

PROJECT_DIR = Path("/content/drive/MyDrive/AngioSimAI")
DATASETS_DIR = PROJECT_DIR / "datasets"
MODELS_DIR = PROJECT_DIR / "models"
RUNS_DIR = PROJECT_DIR / "runs"

DATASET_ZIP = DATASETS_DIR / "roboflow_suture_dataset.zip"
DATASET_DIR = DATASETS_DIR / "roboflow_suture_dataset"
MODEL_PATH = MODELS_DIR / "suture_yolov8_best.pt"

for path in [DATASETS_DIR, MODELS_DIR, RUNS_DIR]:
    path.mkdir(parents=True, exist_ok=True)
```

## Cell 3: install YOLOv8

```python
!pip install ultralytics -q
```

## Cell 4: unzip dataset only when needed

Run this only if `DATASET_DIR` does not already exist or if you uploaded a new dataset zip.

```python
import zipfile

if not DATASET_DIR.exists():
    with zipfile.ZipFile(DATASET_ZIP, "r") as zip_ref:
        zip_ref.extractall(DATASET_DIR)
    print("Dataset extracted:", DATASET_DIR)
else:
    print("Dataset already exists:", DATASET_DIR)
```

## Cell 5: find data.yaml

```python
yaml_files = list(DATASET_DIR.rglob("data.yaml"))
if not yaml_files:
    raise FileNotFoundError("data.yaml not found inside dataset folder")

DATA_YAML = yaml_files[0]
print(DATA_YAML)
```

## Cell 6: train only when needed

Run training only if you do not already have `suture_yolov8_best.pt`, or if you changed the dataset.

```python
from ultralytics import YOLO

if MODEL_PATH.exists():
    print("Model already exists:", MODEL_PATH)
else:
    model = YOLO("yolov8n.pt")
    results = model.train(
        data=str(DATA_YAML),
        epochs=50,
        imgsz=640,
        project=str(RUNS_DIR),
        name="suture_yolov8",
        exist_ok=True,
    )

    trained_best = RUNS_DIR / "suture_yolov8" / "weights" / "best.pt"
    MODEL_PATH.write_bytes(trained_best.read_bytes())
    print("Saved model:", MODEL_PATH)
```

## Cell 7: test existing model without retraining

Use this when you already have `suture_yolov8_best.pt`.

```python
from ultralytics import YOLO

model = YOLO(str(MODEL_PATH))
results = model.predict(
    source="/content/path_to_test_image.jpg",
    conf=0.25,
    save=True,
)
```

## What to send to Codex

Send these when available:

1. `ai_angiosim.ipynb`
2. `data.yaml` content or screenshot
3. class names from Roboflow
4. after training, `suture_yolov8_best.pt`
5. one or two example suture photos for testing

Do not send the whole dataset unless we specifically need to debug dataset structure.
