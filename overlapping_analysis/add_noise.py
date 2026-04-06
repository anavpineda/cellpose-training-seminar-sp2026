import numpy as np
import os
import tifffile as tiff

input_dir = "/nucleus_raw" #and membrane_raw
output_dir ="/nucleus_noisy"
os.makedirs(output_dir, exist_ok=True)

#Edit to change how much noise you want added
mean = 0
sigma = 0.05

for fname in os.listdir(input_dir):
    if fname.lower().endswith((".tiff")):
        path_ = os.path.join(input_dir, fname)

        img = tiff.imread(path_)

        print(fname, img.shape, img.dtype)

        gauss = np.random.normal(mean, sigma, img.shape).astype(np.float32)
        noisy = img.astype(np.float32) + gauss

        # clip before casting
        if img.dtype == np.uint8:
            noisy = np.clip(noisy, 0, 255)
        elif img.dtype == np.uint16:
            noisy = np.clip(noisy, 0, 65535)

        noisy = noisy.astype(img.dtype)

        out_path = os.path.join(output_dir, fname)
        tiff.imwrite(out_path, noisy)

print("Done adding noise to TIFF images.")
