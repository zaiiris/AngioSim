# AI

This folder will contain AI-related work.

Suggested structure:

- `notebooks/` - Colab notebooks and experiments
- `datasets/roboflow/` - Roboflow exports, annotated images, dataset zip files
- `models/` - exported model weights and inference files

For now, put your Colab notebook in `notebooks/` and Roboflow zip/files in `datasets/roboflow/`.

If Colab keeps losing uploaded files after runtime reset, use `COLAB_WORKFLOW.md`.
The key rule is: store dataset zip, extracted dataset, and trained `best.pt` in Google Drive, not only inside the temporary Colab runtime.

## YOLOv8 model file from Colab

After training YOLOv8 in Google Colab, the best weights are usually here:

```text
runs/detect/train/weights/best.pt
```

Sometimes the folder can be `train2`, `train3`, etc. In Colab, run:

```python
!find runs -name best.pt
```

Then download it:

```python
from google.colab import files
files.download("runs/detect/train/weights/best.pt")
```

Rename it locally to:

```text
suture_yolov8_best.pt
```

Put it here:

```text
ai/models/suture_yolov8_best.pt
```

Large model files are ignored by git. Later, store them in Git LFS, a release artifact, Google Drive, or another model storage location.
