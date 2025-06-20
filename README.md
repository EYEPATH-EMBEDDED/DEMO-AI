# 🚦 Collision Predictor

**Real-Time Pedestrian Collision Risk Demo System**

This system combines YOLO-based object detection and Conv-LSTM sequence modeling to **numerically predict collision risk in real-time**, providing visual warnings when the danger threshold is exceeded.

---

## 📦 Installation & Execution

### 1. Install dependencies (virtual environment recommended)

```bash
pip install -r requirements.txt
```

### 2. Prepare model weights

```bash
cp your_last.pt assets/last11.pt
cp first_best_model.pth assets/
```

### 3. Run the demo

#### 🎞️ Video Input

```bash
python run_demo.py src/videos/example.mp4 -o result.mp4
```

#### 🖼️ Image Input (20 FPS, for admin use)

```bash
python run_demo_images.py assets/images -o demo/out_from_images.mp4 --fps 20
```

---

## 🧠 System Pipeline

```
          ┌─────────────────────────────┐
          │     [Image or Video]        │
          └────────────┬────────────────┘
                       ▼
                ┌────────────┐
                │ YOLO Detection │ ← detect_bboxes()
                └────┬─────────┘
                     ▼
              ┌────────────────┐
              │ Feature Builder │ ← build_feature()
              └────┬───────────┘
                   ▼
         ┌────────────────────────────┐
         │ Append to SlidingQueue     │ ← SlidingQueue
         └──────┬─────────────────────┘
                ▼ (300+ frames)
         ┌────────────────────────────┐
         │ Run Conv-LSTM Classifier   │ ← ConvLSTMClassifier
         └──────┬─────────────────────┘
                ▼
     Probability ≥ threshold → 🔴 DANGER
```

---

## 🔍 Core Components

### 🔹 `CollisionPredictor.update()`

> Core function for full prediction pipeline

1. Run YOLO → extract feature vector
2. Append to `SlidingQueue`
3. If 300+ frames, perform Conv-LSTM inference
4. Return class `[1]` probability (i.e., collision)

---

### 🔹 `detect_bboxes(img_bgr, weights_path=...)`

- Runs YOLOv11 detection
- To detect vehicles, modify `classes=[...]` filter

---

### 🔹 `build_feature()`

```python
[
  0.0, 0.0,            # frame_norm, time_norm (default: 0)
  x1 / img_w,
  y1 / img_h,
  x2 / img_w,
  y2 / img_h,
  overlap_ratio(x1, y1, x2, y2),
]
```

---

### 🔹 `SlidingQueue(maxlen=1200)`

- Buffer for time-series model input
- Supports `.append(vec)` and `.as_numpy()`
- Zero-padded for Conv-LSTM compatibility

---

### 🔹 `ConvLSTMClassifier`

- Architecture: Conv1D → Bi-LSTM → FC → Softmax
- Input shape: `(B, T, F=7)`
- Output: `[P(no collision), P(collision)]`

---

## 🎛️ Customization Guide

| Question                              | Modify in...         |
|---------------------------------------|-----------------------|
| Want to detect vehicles?              | `detect_bboxes()` class filter |
| Predict with a single frame?          | Call `update(min_len=1)` |
| Replace Conv-LSTM with another model? | Edit `model.py`       |
| Stream from RTSP in real-time?        | Use `cv2.VideoCapture("rtsp://...")` |
| Need Boolean output only?             | Adjust threshold in `is_danger(prob)` |

---

## 🗂️ Project Structure

```
.
├── run_demo.py
├── run_demo_images.py
├── model.py              # ConvLSTMClassifier definition
├── predictor.py          # CollisionPredictor class
├── detector.py           # YOLO detection functions
├── utils/
│   └── sliding_queue.py  # SlidingQueue utility
├── assets/
│   ├── last11.pt         # YOLO weights
│   ├── first_best_model.pth
│   └── images/           # Input frames
└── demo/
    └── output.mp4        # Inference output
```

---

## 🧾 Requirements

- Python 3.10+
- OpenCV
- PyTorch
- Ultralytics YOLOv11
- NumPy

---

## 📌 Summary

- **Pipeline**: Input → YOLO → Features → Queue → Conv-LSTM → Softmax
- `CollisionPredictor.update()` automates preprocessing and inference
- Needs ~300 frames (~15s) before valid prediction
- Easily extendable and customizable architecture
