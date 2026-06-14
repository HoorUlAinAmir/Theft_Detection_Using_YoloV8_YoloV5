equirements & Installation
System Requirements

Python 3.10 / 3.11 / 3.12
Webcam (built-in or external USB)
OS: Ubuntu / Raspberry Pi OS / Orange Pi OS


Step 1 — System Dependencies
bashsudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv libatlas-base-dev libjpeg-dev libopenblas-dev

Step 2 — Create Virtual Environment
bashpython3 -m venv venv
source venv/bin/activate

Step 3 — Install Python Libraries
For YOLOv8n (main_V8.py):
bashpip install ultralytics
pip install opencv-python
pip install pygame
pip install psutil
pip install numpy
For YOLOv5s (main_V5.py):
bashpip install torch torchvision
pip install opencv-python
pip install pygame
pip install psutil
pip install numpy
pip install pandas

Step 4 — Project Structure
Theft_Detection/
│
├── main_V8.py          # YOLOv8n intrusion detection
├── main_V5.py          # YOLOv5s intrusion detection
├── yolov8n.pt          # YOLOv8n model weights
├── yolov5s.pt          # YOLOv5s model weights
│
├── Alarm/
│   └── alarm.wav       # Alarm sound file
│
└── Detected Photos/    # Auto-created — saved photos
    ├── 1_entry.jpg
    ├── 2_middle_target.jpg
    └── 3_exit.jpg

Step 5 — Run
bash# YOLOv8n
python main_V8.py

# YOLOv5s
python main_V5.py

How to Use
1. Run the script
2. Video window khulega — webcam feed dikhegi
3. Left-click x4  → zone select karo (green area banega)
4. Right-click    → zone reset karo
5. Q (on window)  → quit karo

Notes

Model weights (yolov8n.pt, yolov5s.pt) pehli baar automatically download honge
Detected Photos/ folder automatically create hoga
Alarm sirf tab bajega jab person green zone mein aaye
Benchmark summary terminal mein q dabane ke baad print hogi
