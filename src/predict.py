import os
from ultralytics import YOLO


def inference_task(detect_image_path: str):
    """
    args:
        detect_image_path: str, 待检测图片的路径
    return:
        results: ultralytics.yolo.engine.results.Results, 检测结果对象
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    model = YOLO(
        os.path.join(current_dir, "../runs/detect/chara_finetune/weights/best.pt")
    )

    results = model.predict(source=detect_image_path, conf=0.25, save=True)

    return results

