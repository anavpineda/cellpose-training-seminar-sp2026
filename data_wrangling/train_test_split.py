"""Puts slices into train/test data folders. Neuromasts treated with LY drug are put into the training set. 80/20 split"""
import os
import glob
import shutil
import random

data  = "/Fine_Tune/Slices/"
train_data = "/Fine_Tune/train/"
test_data  = "/Fine_Tune/test/"


os.makedirs(train_data, exist_ok=True)
os.makedirs(test_data, exist_ok=True)

all_images = sorted([
    f for f in glob.glob(os.path.join(data, "*.tiff"))
    if "_masks" not in f
])

for img in all_images:
    if "400ly" in img or "40ly" in img:
        mask = img.replace(".tiff", "_masks.tiff")
        shutil.copy(img, train_data)
        if os.path.exists(mask):
            shutil.copy(mask, train_data)

wt_images = [f for f in all_images if "wt" in f]

random.seed(42)
random.shuffle(wt_images)

split = int(len(wt_images) * 0.8)
wt_train = wt_images[:split]
wt_test  = wt_images[split:]

for img in wt_train:
    mask = img.replace(".tiff", "_masks.tiff")
    shutil.copy(img, train_data)
    if os.path.exists(mask):
        shutil.copy(mask, train_data)

for img in wt_test:
    mask = img.replace(".tiff", "_masks.tiff")
    shutil.copy(img, test_data)
    if os.path.exists(mask):
        shutil.copy(mask, test_data)

print(f"Train: {len(wt_train)} wt + all 40ly/400ly")
print(f"Test:  {len(wt_test)} wt")
