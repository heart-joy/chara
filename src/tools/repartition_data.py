import os
import shutil

categories = [
    "Anti-Aircraft-Gun",
    "Bomber",
    "Fighter-Jet",
    "Fixed-Wing",
    "Helicopter",
    "Machine-Gunner",
    "Reconnaissance-Plane",
    "Rocket-Soldier",
    "Rotary-Wing",
    "Tank",
    "Transport-Plane",
    "Truck",
]

val_img_dir = "datasets/val/images"
val_lbl_dir = "datasets/val/labels"
train_img_dir = "datasets/train/images"
train_lbl_dir = "datasets/train/labels"

# Ensure train directories exist
os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(train_lbl_dir, exist_ok=True)

for cat in categories:
    # Find all images for this category in val
    imgs = [
        f
        for f in os.listdir(val_img_dir)
        if f.startswith(cat + "_") and f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]
    imgs.sort()

    if len(imgs) == 20:
        # Move 18 to train, keep 2 in val
        to_move = imgs[:18]
        for img_name in to_move:
            # Move image
            src_img = os.path.join(val_img_dir, img_name)
            dst_img = os.path.join(train_img_dir, img_name)
            shutil.move(src_img, dst_img)

            # Move corresponding label
            base_name = os.path.splitext(img_name)[0]
            lbl_name = base_name + ".txt"
            src_lbl = os.path.join(val_lbl_dir, lbl_name)
            dst_lbl = os.path.join(train_lbl_dir, lbl_name)

            if os.path.exists(src_lbl):
                shutil.move(src_lbl, dst_lbl)
            else:
                print(f"Warning: Label not found for {img_name}")
        print(f"Moved 18 files for category: {cat}")
    else:
        print(
            f"Category {cat} does not have exactly 20 images (found {len(imgs)}), skipping."
        )

"""
Danger: 尚未经过审核
"""
