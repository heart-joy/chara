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

    root_dir = os.path.dirname(current_dir) 

    model = YOLO(
        os.path.join(current_dir, "../runs/detect/chara_finetune/weights/best.pt") #拼接的应该是current_dir和模型权重文件的相对路径
    )

    results = model.predict(source=detect_image_path, conf=0.25, save=True)

    return results

results = inference_task(r"C:\Users\86138\Desktop\yolo\datasets\train\images\digit_12.png")
