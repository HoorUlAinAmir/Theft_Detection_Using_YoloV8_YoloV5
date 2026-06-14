##🔒 Theft Detection System

Real-time intrusion detection using YOLOv8n and YOLOv5s with webcam support, 
zone-based alerting, alarm system, and benchmarking.

---

## 📋 Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [Benchmarking](#benchmarking)
- [Notes](#notes)

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

### Step 3 — Install Libraries

**YOLOv8n** (`main_V8.py`):
```bash
pip install ultralytics opencv-python pygame psutil numpy
```

**YOLOv5s** (`main_V5.py`):
```bash
pip install torch torchvision opencv-python pygame psutil numpy pandas
```

---

## 📁 Project Structure
Theft_Detection/

│

├── main_V8.py              # YOLOv8n — intrusion detection

├── main_V5.py              # YOLOv5s — intrusion detection

├── yolov8n.pt              # YOLOv8n model weights

├── yolov5s.pt              # YOLOv5s model weights

│

├── Alarm/

│   └── alarm.wav           # Alarm sound

│

└── Detected Photos/        # Auto-created on first detection

├── 1_entry.jpg         # Person enters zone

├── 2_middle_target.jpg # Person inside zone

└── 3_exit.jpg          # Person exits zone

---

## ▶️ How to Run

```bash
# Activate virtual environment first
source venv/bin/activate

# Run YOLOv8n version
python main_V8.py

# Run YOLOv5s version
python main_V5.py
```

---

## 🖱️ How to Use

| Action | Result |
|--------|--------|
| Left-click × 4 | Draw detection zone (green area) |
| Right-click | Reset / clear zone |
| `Q` key (on video window) | Quit the program |

> ⚠️ Press `Q` on the **video window**, not in the terminal.

---

## 📊 Benchmarking

Live stats are printed in terminal every 30 frames:
--- Frame 30 ---

FPS         : 6.1

Inference   : 156.1 ms

Preproc     : 0.4 ms

Postproc    : 0.5 ms

Detections  : 1

Person Zone : No

Final summary prints when you press `Q`:
=============================================

FINAL BENCHMARK SUMMARY
Total Frames       : 160

Avg FPS            : 6.23

Avg Inference      : 154.49 ms

Avg Preprocessing  : 0.44 ms

Avg Postprocessing : 0.64 ms

Avg Detections     : 1.41 /frame

Model Size         : 6.25 MB

RAM Usage          : 796 MB

---

## 📸 Photo Capture

3 photos are automatically saved when a person is detected in the zone:

| File | When Saved |
|------|-----------|
| `1_entry.jpg` | Person enters the zone |
| `2_middle_target.jpg` | Person inside zone (after 30 frames) |
| `3_exit.jpg` | Person exits the zone |

---

## 📝 Notes

- Model weights download automatically on first run (~6MB for YOLOv8n, ~14MB for YOLOv5s)
- `Detected Photos/` folder is created automatically
- Alarm triggers only when person enters the green zone
- All warnings in terminal can be ignored — they do not affect performance
- For better performance on Raspberry Pi / Orange Pi, use **YOLOv8n** (faster than YOLOv5s)
