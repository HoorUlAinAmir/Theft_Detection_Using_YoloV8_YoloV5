# 🔒 Theft Detection System

Real-time intrusion detection using YOLOv8n and YOLOv5n with webcam support,
zone-based alerting, alarm system, and performance benchmarking.

---

## 📋 Table of Contents
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [How to Use](#-how-to-use)
- [Benchmarking](#-benchmarking)
- [Photo Capture](#-photo-capture)
- [Notes](#-notes)

---

## 💻 Requirements

| Component | Details |
|-----------|---------|
| Python | 3.10 / 3.11 / 3.12 |
| Camera | Built-in or External USB Webcam |
| OS | Ubuntu / Raspberry Pi OS / Orange Pi OS |
| RAM | Minimum 2GB recommended |

---

## ⚙️ Installation

### Step 1 — Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv libatlas-base-dev libjpeg-dev libopenblas-dev
```

### Step 2 — Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Python Libraries

**For YOLOv8n** (`main_V8.py`):
```bash
pip install ultralytics opencv-python pygame psutil numpy
```

**For YOLOv5n** (`main_V5.py`):
```bash
pip install torch torchvision opencv-python pygame psutil numpy pandas
```

---

## 📁 Project Structure

```
Theft_Detection/
│
├── main_V8.py              # YOLOv8n — intrusion detection
├── main_V5.py              # YOLOv5n — intrusion detection
├── yolov8n.pt              # YOLOv8n model weights
├── yolov5n.pt              # YOLOv5n model weights
│
├── Alarm/
│   └── alarm.wav           # Alarm sound file
│
└── Detected Photos/        # Auto-created on first detection
    ├── 1_entry.jpg         # Photo when person enters zone
    ├── 2_middle_target.jpg # Photo when person is inside zone
    └── 3_exit.jpg          # Photo when person exits zone
```

---

## ▶️ How to Run

```bash
# Step 1 — Activate virtual environment
source venv/bin/activate

# Step 2 — Run YOLOv8n version (recommended)
python main_V8.py

# OR — Run YOLOv5s version
python main_V5.py
```

---

## 🖱️ How to Use

| Action | Result |
|--------|--------|
| **Left-click × 4** | Draw detection zone (green area appears) |
| **Right-click** | Reset and clear the zone |
| **`Q` key** (on video window) | Quit the program |

> ⚠️ **Important:** Press `Q` on the **video window**, not in the terminal.

**Zone Drawing Tips:**
- Click 4 points to form a rectangle around the area you want to monitor
- Click in this order for best results:

```
Point 1 (top-left) -------- Point 2 (top-right)
        |                           |
Point 4 (bottom-left) ----- Point 3 (bottom-right)
```

- If zone looks wrong → **right-click** to reset and try again

---

## 📊 Benchmarking

Live benchmark stats are printed in terminal every 30 frames automatically:

```
--- Frame 30 ---
  FPS         : 6.1
  Inference   : 156.1 ms
  Preproc     : 0.4 ms
  Postproc    : 0.5 ms
  Detections  : 1
  Person Zone : No

--- Frame 60 ---
  FPS         : 6.4
  Inference   : 150.2 ms
  Preproc     : 0.4 ms
  Postproc    : 0.5 ms
  Detections  : 1
  Person Zone : YES - ALARM!
```

Final summary is printed when you press `Q`:

```
=============================================
       FINAL BENCHMARK SUMMARY
=============================================
  Total Frames       : 160
  Avg FPS            : 6.23
  Avg Inference      : 154.49 ms
  Avg Preprocessing  : 0.44 ms
  Avg Postprocessing : 0.64 ms
  Avg Detections     : 1.41 /frame
  Model Size         : 6.25 MB
  RAM Usage          : 796 MB
  Photos Saved       : entry + middle + exit = 3
=============================================
```

### Benchmark Metrics Explained

| Metric | Description |
|--------|-------------|
| **FPS** | Frames processed per second. Higher = smoother |
| **Inference** | Time taken by model to detect objects (ms) |
| **Preproc** | Image preprocessing time before detection (ms) |
| **Postproc** | Time to process detection results (ms) |
| **Avg Detections** | Average persons detected per frame |
| **Model Size** | Storage size of the model file |
| **RAM Usage** | Memory used during runtime |

---

## 📸 Photo Capture

Exactly **3 photos** are saved automatically per session:

| File | When Saved |
|------|-----------|
| `1_entry.jpg` | The moment person **enters** the zone |
| `2_middle_target.jpg` | Person **inside** zone after 30 frames |
| `3_exit.jpg` | The moment person **exits** the zone |

> Photos are saved in `Detected Photos/` folder (auto-created).

---

## 📝 Notes

- Model weights download **automatically** on first run
  - YOLOv8n → ~6 MB
  - YOLOv5n → ~14 MB
- `Detected Photos/` folder is created automatically — no manual setup needed
- Alarm triggers **only** when a person enters the green zone
- All `FutureWarning` messages in terminal are harmless — they do not affect performance
- For **Raspberry Pi / Orange Pi**, use `main_V8.py` (YOLOv8n) — it is faster and lighter than YOLOv5s

---

## 📈 Model Comparison

| Model | Size | Avg FPS | Avg Inference | RAM Usage |
|-------|------|---------|---------------|-----------|
| YOLOv8n | 6.25 MB | ~6.2 | ~154 ms | ~796 MB |
| YOLOv5n | 14.12 MB | ~4.0 | ~247 ms | ~946 MB |

> Tested on ThinkPad T440p — CPU only, no GPU.
