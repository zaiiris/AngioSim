from __future__ import annotations

import hashlib
import json
import math
from functools import lru_cache
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = ROOT_DIR / "backend" / "uploads" / "suture_images"
MODEL_PATH = ROOT_DIR / "ai" / "models" / "suture_yolov8_best.pt"
VESSEL_DIAMETER_MM = 5.0


@dataclass(frozen=True)
class AiAnalysis:
    osats_score: float
    stitch_count: int
    uniformity_percent: int
    confidence: float
    feedback: str
    raw_predictions: dict


def analyze_suture_image(image_path: Path) -> AiAnalysis:
    if MODEL_PATH.exists():
        try:
            return analyze_suture_image_yolo(image_path)
        except Exception as exc:
            mock = analyze_suture_image_mock(image_path)
            mock.raw_predictions["fallback_reason"] = str(exc)
            return mock

    return analyze_suture_image_mock(image_path)


def analyze_suture_image_mock(image_path: Path) -> AiAnalysis:
    """Deterministic fallback used when YOLO dependencies or weights are unavailable."""
    digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
    seed = int(digest[:8], 16)

    stitch_count = 6 + seed % 5
    uniformity = 66 + seed % 27
    osats = round(3.2 + (uniformity - 60) / 35, 1)
    osats = min(osats, 5.0)
    confidence = round(0.78 + (seed % 18) / 100, 2)

    if uniformity >= 86:
        feedback = "Good suture rhythm. Keep the same spacing and needle angle."
    elif uniformity >= 75:
        feedback = "Suture quality is stable, but spacing can be more even."
    else:
        feedback = "Spacing is uneven. Try to keep each stitch interval close to 0.8-1.0 mm."

    return AiAnalysis(
        osats_score=osats,
        stitch_count=stitch_count,
        uniformity_percent=uniformity,
        confidence=confidence,
        feedback=feedback,
        raw_predictions={
            "mode": "mock",
            "model": str(MODEL_PATH),
            "detections": [
                {"class": "stitch", "count": stitch_count, "confidence": confidence}
            ],
        },
    )


@lru_cache(maxsize=1)
def load_yolo_model():
    from ultralytics import YOLO

    return YOLO(str(MODEL_PATH))


def analyze_suture_image_yolo(image_path: Path) -> AiAnalysis:
    model = load_yolo_model()
    results = model.predict(source=str(image_path), conf=0.25, save=False, verbose=False)
    if not results:
        return yolo_empty_result("No prediction result returned")

    result = results[0]
    boxes = []
    confidences = []

    for box in result.boxes:
        x_center, y_center, width, height = box.xywhn[0].tolist()
        confidence = float(box.conf[0].item())
        class_id = int(box.cls[0].item())
        boxes.append(
            {
                "x_center": float(x_center),
                "y_center": float(y_center),
                "width": float(width),
                "height": float(height),
                "confidence": confidence,
                "class_id": class_id,
            }
        )
        confidences.append(confidence)

    metrics = calculate_suture_metrics(boxes, result.orig_shape)
    confidence = round(sum(confidences) / len(confidences), 2) if confidences else 0.0
    feedback = build_feedback(metrics)

    return AiAnalysis(
        osats_score=metrics["osats_score_5"],
        stitch_count=metrics["stitch_count"],
        uniformity_percent=metrics["uniformity_percent"],
        confidence=confidence,
        feedback=feedback,
        raw_predictions={
            "mode": "yolov8",
            "model": str(MODEL_PATH),
            "image_shape": {
                "height": result.orig_shape[0],
                "width": result.orig_shape[1],
            },
            "detections": boxes,
            "metrics": metrics,
        },
    )


def yolo_empty_result(reason: str) -> AiAnalysis:
    return AiAnalysis(
        osats_score=0.0,
        stitch_count=0,
        uniformity_percent=0,
        confidence=0.0,
        feedback="No stitches were detected. Try a clearer photo with the suture centered.",
        raw_predictions={
            "mode": "yolov8",
            "model": str(MODEL_PATH),
            "reason": reason,
            "detections": [],
        },
    )


def calculate_suture_metrics(boxes: list[dict], image_shape: tuple[int, int]) -> dict:
    stitch_count = len(boxes)
    if stitch_count < 2:
        return {
            "stitch_count": stitch_count,
            "osats_score_100": 0,
            "osats_score_5": 0.0,
            "uniformity_percent": 0,
            "mean_distance_mm": 0,
            "min_distance_mm": 0,
            "max_distance_mm": 0,
            "std_distance_mm": 0,
            "gaps": [],
        }

    image_h, image_w = image_shape
    points = []
    for box in boxes:
        points.append(
            {
                **box,
                "cx_px": box["x_center"] * image_w,
                "cy_px": box["y_center"] * image_h,
                "w_px": box["width"] * image_w,
                "h_px": box["height"] * image_h,
            }
        )
    points.sort(key=lambda item: item["cx_px"])

    y_span_px = max(p["cy_px"] for p in points) - min(p["cy_px"] for p in points)
    calibration_method = "Y-span stitches"
    if y_span_px < 10:
        y_span_px = max(p["h_px"] for p in points)
        calibration_method = "bbox height"

    px_per_mm = y_span_px / VESSEL_DIAMETER_MM if y_span_px > 0 else 1
    distances_mm = []
    for left, right in zip(points, points[1:]):
        dx = right["cx_px"] - left["cx_px"]
        dy = right["cy_px"] - left["cy_px"]
        distances_mm.append(math.sqrt(dx * dx + dy * dy) / px_per_mm)

    mean_distance = sum(distances_mm) / len(distances_mm)
    variance = sum((value - mean_distance) ** 2 for value in distances_mm) / len(distances_mm)
    std_distance = math.sqrt(variance)
    uniformity = max(0.0, 1 - std_distance / mean_distance) if mean_distance > 0 else 0.0

    widths_mm = [p["w_px"] / px_per_mm for p in points]
    mean_width = sum(widths_mm) / len(widths_mm)
    width_variance = sum((value - mean_width) ** 2 for value in widths_mm) / len(widths_mm)
    width_std = math.sqrt(width_variance)
    size_uniformity = max(0.0, 1 - (width_std / mean_width)) if mean_width > 0 else 0.0

    mean_y_mm = sum(p["cy_px"] / px_per_mm for p in points) / len(points)
    deviations = [abs((p["cy_px"] / px_per_mm) - mean_y_mm) for p in points]
    mean_deviation = sum(deviations) / len(deviations)
    line_score = max(0, 100 - (mean_deviation / VESSEL_DIAMETER_MM) * 100)

    gap_threshold = mean_distance + 2 * std_distance
    gaps = [
        {
            "from_stitch": index + 1,
            "to_stitch": index + 2,
            "distance_mm": round(distance, 2),
        }
        for index, distance in enumerate(distances_mm)
        if distance > gap_threshold
    ]

    count_score = 100 if 8 <= stitch_count <= 12 else max(0, 100 - abs(stitch_count - 10) * 7)
    osats_100 = max(
        0,
        round(
            count_score * 0.25
            + uniformity * 100 * 0.40
            + size_uniformity * 100 * 0.20
            + line_score * 0.15
            - len(gaps) * 8,
            1,
        ),
    )

    return {
        "stitch_count": stitch_count,
        "osats_score_100": osats_100,
        "osats_score_5": round(osats_100 / 20, 1),
        "uniformity_percent": round(uniformity * 100),
        "mean_distance_mm": round(mean_distance, 2),
        "min_distance_mm": round(min(distances_mm), 2),
        "max_distance_mm": round(max(distances_mm), 2),
        "std_distance_mm": round(std_distance, 2),
        "size_uniformity_percent": round(size_uniformity * 100),
        "mean_line_deviation_mm": round(mean_deviation, 2),
        "gaps": gaps,
        "calibration_method": calibration_method,
        "px_per_mm": round(px_per_mm, 2),
    }


def build_feedback(metrics: dict) -> str:
    if metrics["stitch_count"] < 2:
        return "No stitches were detected. Try a clearer photo with the suture centered."
    if metrics["uniformity_percent"] >= 85:
        return "Spacing is stable. Keep the same rhythm and needle angle."
    if metrics["uniformity_percent"] >= 70:
        return "Suture quality is acceptable, but spacing can be more even."
    return "Spacing is uneven. Try to keep stitch intervals more consistent."


def save_upload(session_id: int, filename: str, content: bytes) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(filename).suffix.lower() or ".jpg"
    safe_path = UPLOAD_DIR / f"session_{session_id}_{hashlib.sha1(content).hexdigest()[:12]}{suffix}"
    safe_path.write_bytes(content)
    return safe_path


def analysis_to_json(analysis: AiAnalysis) -> str:
    return json.dumps(analysis.raw_predictions, ensure_ascii=False)
