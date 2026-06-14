import cv2
import torch
import numpy as np
import pygame
import time
import psutil
import os
import warnings
warnings.filterwarnings("ignore")
# ─── ALARM SETUP ───────────────────────────────────────────
path_alarm = "Alarm/alarm.wav"
pygame.init()
pygame.mixer.music.load(path_alarm)

# ─── MODEL SETUP ───────────────────────────────────────────
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
cap = cv2.VideoCapture(2)
target_classes = ['person']

# ─── PHOTO TRACKING ────────────────────────────────────────
photo_entry_saved  = False
photo_middle_saved = False
photo_exit_saved   = False
middle_frame_count = 0
was_in_zone        = False

pts = []

# ─── BENCHMARK VARIABLES ───────────────────────────────────
fps_list        = []
inference_times = []
preprocess_times= []
postprocess_times=[]
detection_counts= []
prev_time       = time.time()
frame_number    = 0

model_size_mb = os.path.getsize('yolov5s.pt') / (1024 * 1024)

# ─── FUNCTIONS ─────────────────────────────────────────────
def order_points(pts_list):
    pts_arr = np.array(pts_list)
    s    = pts_arr.sum(axis=1)
    diff = np.diff(pts_arr, axis=1)
    ordered = np.zeros((4, 2), dtype=int)
    ordered[0] = pts_arr[np.argmin(s)]
    ordered[2] = pts_arr[np.argmax(s)]
    ordered[1] = pts_arr[np.argmin(diff)]
    ordered[3] = pts_arr[np.argmax(diff)]
    return ordered.tolist()

def draw_polygon(event, x, y, flags, param):
    global pts
    if event == cv2.EVENT_LBUTTONDOWN:
        pts.append([x, y])
        if len(pts) == 4:
            pts = order_points(pts)
            print(f"\n[ZONE SET] Points: {pts}")
    elif event == cv2.EVENT_RBUTTONDOWN:
        pts = []
        print("[ZONE RESET] Points clear ho gaye")

def inside_polygon(point, polygon):
    result = cv2.pointPolygonTest(polygon, (point[0], point[1]), False)
    return result == 1

def preprocess(img):
    height, width = img.shape[:2]
    ratio = height / width
    img = cv2.resize(img, (640, int(640 * ratio)))
    return img

def save_photo(frame, label):
    os.makedirs("Detected Photos", exist_ok=True)
    filename = f"Detected Photos/{label}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[PHOTO SAVED] {filename}")

def print_live_stats(frame_number, fps, inf_ms, pre_ms, post_ms,
                     det_count, person_in_zone):
    if frame_number % 30 == 0:
        print(f"\n--- Frame {frame_number} ---")
        print(f"  FPS         : {fps:.1f}")
        print(f"  Inference   : {inf_ms:.1f} ms")
        print(f"  Preproc     : {pre_ms:.1f} ms")
        print(f"  Postproc    : {post_ms:.1f} ms")
        print(f"  Detections  : {det_count}")
        print(f"  Person Zone : {'YES - ALARM!' if person_in_zone else 'No'}")

# ─── MAIN LOOP ─────────────────────────────────────────────
cv2.namedWindow('Video')
cv2.setMouseCallback('Video', draw_polygon)

print("\n[START] YOLOv5s system chal raha hai...")
print(f"[INFO]  Model Size : {model_size_mb:.2f} MB")
print("[INFO]  Q dabao band karne ke liye\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_number += 1

    # ── Preprocessing ──────────────────────────────────────
    t_pre_start  = time.time()
    frame_detected = frame.copy()
    frame        = preprocess(frame)
    t_pre_end    = time.time()
    pre_ms       = (t_pre_end - t_pre_start) * 1000

    # ── Polygon draw ───────────────────────────────────────
    if len(pts) >= 4:
        frame_copy = frame.copy()
        cv2.fillPoly(frame_copy, np.array([pts]), (0, 200, 0))
        frame = cv2.addWeighted(frame_copy, 0.5, frame, 0.5, 0)
        cv2.polylines(frame, np.array([pts], dtype=np.int32), True, (0, 255, 0), 3)

    # ── Inference ──────────────────────────────────────────
    t_inf_start = time.time()
    results     = model(frame)
    t_inf_end   = time.time()
    inf_ms      = (t_inf_end - t_inf_start) * 1000
    inference_times.append(inf_ms)

    # ── Postprocessing + Detection ─────────────────────────
    t_post_start    = time.time()
    person_in_zone  = False
    frame_det_count = 0

    for index, row in results.pandas().xyxy[0].iterrows():
        center_x = None
        center_y = None

        if row['name'] in target_classes:
            frame_det_count += 1
            name = str(row['name'])
            x1   = int(row['xmin'])
            y1   = int(row['ymin'])
            x2   = int(row['xmax'])
            y2   = int(row['ymax'])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)
            cv2.putText(frame, name, (x1, y1),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            if len(pts) >= 4:
                if inside_polygon((center_x, center_y), np.array([pts])):
                    person_in_zone  = True
                    middle_frame_count += 1

                    cv2.putText(frame, "Target", (center_x, center_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    cv2.putText(frame, "Person Detected", (20, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 3)

                    # ── ENTRY photo ────────────────────────
                    if not was_in_zone and not photo_entry_saved:
                        save_photo(frame, "1_entry")
                        photo_entry_saved = True
                        print("[EVENT] Person ne zone enter kiya!")

                    # ── MIDDLE photo (30 frames baad) ──────
                    if middle_frame_count == 30 and not photo_middle_saved:
                        save_photo(frame, "2_middle_target")
                        photo_middle_saved = True
                        print("[EVENT] Person zone ke andar hai!")

                    # ── Alarm ──────────────────────────────
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
                        print("[ALARM] Bajaya!")

                    mask   = np.zeros_like(frame_detected)
                    points = np.array([[x1,y1],[x1,y2],[x2,y2],[x2,y1]])
                    points = points.reshape((-1, 1, 2))
                    mask   = cv2.fillPoly(mask, [points], (255, 255, 255))
                    frame_detected = cv2.bitwise_and(frame_detected, mask)

    # ── EXIT photo ─────────────────────────────────────────
    if was_in_zone and not person_in_zone and not photo_exit_saved:
        save_photo(frame, "3_exit")
        photo_exit_saved = True
        print("[EVENT] Person zone se nikla!")

    was_in_zone = person_in_zone

    t_post_end = time.time()
    post_ms    = (t_post_end - t_post_start) * 1000
    postprocess_times.append(post_ms)
    detection_counts.append(frame_det_count)
    preprocess_times.append(pre_ms)

    # ── FPS ────────────────────────────────────────────────
    curr_time = time.time()
    fps       = 1.0 / (curr_time - prev_time + 1e-9)
    prev_time = curr_time
    fps_list.append(fps)

    avg_fps  = sum(fps_list[-30:])         / len(fps_list[-30:])
    avg_inf  = sum(inference_times[-30:])  / len(inference_times[-30:])
    avg_pre  = sum(preprocess_times[-30:]) / len(preprocess_times[-30:])
    avg_post = sum(postprocess_times[-30:])/ len(postprocess_times[-30:])

    print_live_stats(frame_number, avg_fps, avg_inf,
                     avg_pre, avg_post, frame_det_count, person_in_zone)

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n[QUIT] Band ho raha hai...")
        break

# ─── FINAL BENCHMARK SUMMARY ───────────────────────────────
mem = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

print("\n" + "="*45)
print("       FINAL BENCHMARK SUMMARY (YOLOv5s)")
print("="*45)
print(f"  Total Frames       : {len(fps_list)}")
print(f"  Avg FPS            : {sum(fps_list)/len(fps_list):.2f}")
print(f"  Avg Inference      : {sum(inference_times)/len(inference_times):.2f} ms")
print(f"  Avg Preprocessing  : {sum(preprocess_times)/len(preprocess_times):.2f} ms")
print(f"  Avg Postprocessing : {sum(postprocess_times)/len(postprocess_times):.2f} ms")
print(f"  Avg Detections     : {sum(detection_counts)/len(detection_counts):.2f} /frame")
print(f"  Model Size         : {model_size_mb:.2f} MB")
print(f"  RAM Usage          : {mem:.0f} MB")
print(f"  Photos Saved       : entry + middle + exit = 3")
print("="*45 + "\n")

cap.release()
cv2.destroyAllWindows()
