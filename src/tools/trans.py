# 生成一段代码，获取特定目录下的图片，并生成对应的标签文件到特定的目录下，标签文件的格式为class_id center_x center_y width height
# #class_id：类别 ID（从 0 开始）
# center_x, center_y：边界框中心点的归一化坐标（0-1）
# width, height：边界框的归一化宽度和高度（0-1）
import cv2
import numpy as np
import os

class_lib = ["digit_01","digit_02","digit_03","digit_04","digit_05","digit_06","digit_07","digit_08","digit_09","digit_10","digit_11","digit_12","digit_13","digit_14","digit_15","digit_16","digit_17","digit_18","digit_19","digit_20","digit_21","digit_22","digit_23","digit_24","digit_25","digit_26","digit_27","digit_28","digit_29","digit_30","digit_31","digit_32","digit_33","digit_34","digit_35","digit_36","digit_37","digit_38","digit_39","digit_40","digit_41","digit_42","digit_43","digit_44","digit_45","digit_46","digit_47","digit_48","digit_49","digit_50","digit_51","digit_52","digit_53","digit_54","digit_55","digit_56","digit_57","digit_58","digit_59","digit_60","digit_61","digit_62","digit_63","digit_64","digit_65","digit_66","digit_67","digit_68","digit_69","digit_70","digit_71","digit_72","digit_73","digit_74","digit_75","digit_76","digit_77","digit_78","digit_79","digit_80","digit_81","digit_82","digit_83","digit_84","digit_85","digit_86","digit_87","digit_88","digit_89","digit_90","digit_91","digit_92","digit_93","digit_94","digit_95","digit_96","digit_97","digit_98","digit_99","Rotary-Wing", "Anti-Aircraft-Gun", "Fixed-Wing", "Bomber", "Rocket-Soldier", "Machine-Gunner", "Truck", "Tank", "Transport-Plane", "Fighter-Jet", "Reconnaissance-Plane", "Helicopter"]

def get_target_bbox(img_path):

    img = cv2.imread(img_path)

    if img is None:
        return None

    # 已统一为640×640
    IMG_SIZE = 640

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 红色HSV范围
    lower_red1 = np.array([0, 80, 80])
    upper_red1 = np.array([15, 255, 255])

    lower_red2 = np.array([160, 80, 80])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = cv2.bitwise_or(mask1, mask2)

    # 去噪
    kernel = np.ones((5, 5), np.uint8)

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

    if len(contours) == 0:
        return None

    center_x = IMG_SIZE / 2
    center_y = IMG_SIZE / 2

    best_contour = None
    best_score = float("inf")

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area < 100:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        cx = x + w / 2
        cy = y + h / 2

        # 优先选择靠近中心的红色目标
        dist = np.sqrt(
            (cx - center_x) ** 2 +
            (cy - center_y) ** 2
        )

        if dist < best_score:
            best_score = dist
            best_contour = cnt

    if best_contour is None:
        return None

    x, y, w, h = cv2.boundingRect(best_contour)

    # YOLO格式
    cx = (x + w / 2) / IMG_SIZE
    cy = (y + h / 2) / IMG_SIZE

    nw = w / IMG_SIZE
    nh = h / IMG_SIZE

    return cx, cy, nw, nh


if __name__ == "__main__":

    image_dir = r"C:\Users\86138\Desktop\yolo\datasets\val\images"
    label_dir = r"C:\Users\86138\Desktop\yolo\datasets\val\labels"

    os.makedirs(label_dir, exist_ok=True)

    for files in os.listdir(image_dir):

        if not files.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(image_dir, files)

        result = get_target_bbox(img_path)

        class_name = files.split("_")[0]

        if class_name not in class_lib:
            continue

        class_id = class_lib.index(class_name)

        label_path = os.path.join(
            label_dir,
            os.path.splitext(files)[0] + ".txt"
        )

        with open(label_path, "w") as f:

            if result is not None:

                cx, cy, nw, nh = result

                f.write(f"{class_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")
