import cv2
import numpy as np


def coarse_detect(img):

    hsv = cv2.cvtColor(img,
                       cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 80, 80])
    upper_red1 = np.array([15, 255, 255])

    lower_red2 = np.array([160, 80, 80])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv,
                        lower_red1,
                        upper_red1)

    mask2 = cv2.inRange(hsv,
                        lower_red2,
                        upper_red2)

    mask = cv2.bitwise_or(mask1,
                          mask2)

    kernel = np.ones((5, 5),
                     np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    candidates = []

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 80:
            continue

        if area > 20000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        ratio = w / h

        if ratio < 0.2:
            continue

        if ratio > 5:
            continue

        side = int(max(w, h) * 2)

        cx = x + w // 2
        cy = y + h // 2

        x1 = max(cx - side // 2,
                 0)

        y1 = max(cy - side // 2,
                 0)

        x2 = min(cx + side // 2,
                 img.shape[1])

        y2 = min(cy + side // 2,
                 img.shape[0])

        candidates.append(
            (x1, y1, x2, y2)
        )

    return candidates

if __name__ == "__main__":
    img = cv2.imread(r"C:\Users\86138\Desktop\yolo\chara\datasets\val\images\Truck_005.jpg")

    boxes = coarse_detect(img)

    for i, (x1, y1, x2, y2) in enumerate(boxes):

        crop = img[y1:y2,
                x1:x2]

        cv2.imwrite(
            f"candidate_{i}.jpg",
            crop
        )