import os

from ultralytics import YOLO


def train_custom_model():

    current_dir = os.path.dirname(os.path.abspath(__file__))

    root_dir = os.path.dirname(current_dir)

    yaml_path = os.path.join(current_dir, "yolo.yaml")
    model_path = os.path.join(current_dir, "yolo26n.pt")

    model = YOLO(model_path)

    results = model.train(
        data=yaml_path,
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,
        workers=8,
        degrees=10.0,
        translate=0.1,
        scale=0.5,
        shear=2.0,
        perspective=0.0001,
        flipud=0.5,
        fliplr=0.5,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        erasing=0.4,
        copy_paste=0.1,
        val=True,
        optimizer="AdamW",
        amp=True,
        exist_ok=True,
        project=os.path.join(root_dir, "runs/detect"),
        name="chara_finetune",
    )


if __name__ == "__main__":
    train_custom_model()
