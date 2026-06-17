import os
import cv2
import time
import datetime

def img_capture():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error:Cannot open camera")
        return None
    for i in range(100):
        ret, frame = cam.read()
        if not ret:
            print("Error:Cannot read frame from camera")
            break
        filename = f"./chara/workspace/capture-img/captured_{i}.jpg"
        start_time = time.time()
        cv2.imwrite(filename,frame)
        end_time = time.time()
        time.sleep(max(0.05,0.05-(end_time-start_time)))
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img_capture()
