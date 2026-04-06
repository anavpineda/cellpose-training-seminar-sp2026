import numpy as np
from cellpose import models, io
from skimage.util import invert
import tifffile
import os

"""Code used to test the model and make predicitons
Inputs: Membrane directory of membrane tiffs
        Nuclei directory of nuclei tiffs
        Model path
        Output: Folder of predicitions"""
io.logger_setup()

membrane_dir = "/membrane"
nucleus_dir  = "/nucleus"
output_path  = "/predictions"
model_path   = "/neuromast_cellpose_trained_model"

model = models.CellposeModel(pretrained_model=model_path, gpu=True)

for file_name in os.listdir(nucleus_dir):
    nuclei_path   = os.path.join(nucleus_dir, file_name)
    membrane_path = os.path.join(membrane_dir, file_name)

    nuclei   = invert(io.imread(nuclei_path))
    membrane = io.imread(membrane_path)

    # stacking error was returning "no pixels found"
    img = np.stack([nuclei, membrane], axis=-1)

    print(f"Processing: {file_name}")
    masks, flows, styles = model.eval(
        img,
        diameter=None,
        channels=[1, 2],        # ch1=membrane (cell body), ch2=nuclei
        stitch_threshold=0.5,
        z_axis=0,
        channel_axis=3
    )

    masks = np.array(masks, dtype=np.int32)
    tifffile.imwrite(os.path.join(output_path, file_name), masks)
