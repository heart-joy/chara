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
        epochs=200,
        imgsz=960,
        batch=8,
        device=0,
        workers=8,
        optimizer="auto",
        amp=True,
        mosaic=0.3,
        close_mosaic=20,
        mixup=0.0,
        copy_paste=0.0,
        erasing=0.0,
        degrees=5.0,
        translate=0.1,
        scale=0.3,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        val=True,
        plots=True,
        exist_ok=True,
        project=os.path.join(root_dir, "runs/detect"),
        name="chara_finetune",
    )


if __name__ == "__main__":
    train_custom_model()
