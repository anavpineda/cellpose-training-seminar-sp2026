import numpy as np
import matplotlib.pyplot as plt
from cellpose import models, io
from cellpose.io import imread
from skimage.util import invert
from skimage import io as skio
import os
io.logger_setup()

nuclei_path = "/hpc/projects/jacobo_group/iSim_processed_files/HCR/2025-06-25_N2V_model_training_tif/final_hcr_results/dla/dmso/denoised/tiffs/fish_dmsobdlafish1/she_2.tiff"
membrane_path = "/hpc/projects/jacobo_group/iSim_processed_files/HCR/2025-06-25_N2V_model_training_tif/final_hcr_results/dla/dmso/denoised/tiffs/fish_dmsobdlafish1/membrane_2.tiff"
model_path = "/hpc/projects/jacobo_group/projects/cellpose/Membranes/2_Channel/HCR/Fine_Tune/models/neuromast_cellpose_trained_model"
output_path = "/hpc/projects/jacobo_group/projects/cellpose/Membranes/2_Channel/HCR/Fine_Tune/final_outputs"

nuclei = imread(nuclei_path)
membrane = imread(membrane_path)

img = np.zeros((2, nuclei.shape[0], nuclei.shape[1], nuclei.shape[2]), dtype=np.uint16)
img[0,:,:,:] = nuclei
img[1,:,:,:] = membrane

model = models.CellposeModel(pretrained_model=model_path, gpu=True)
masks, flows, styles = model.eval(img, diameter=None, channels=[1,2], stitch_threshold=0.5, channel_axis=0, z_axis=1)

save_name = os.path.join(output_path, "dmsodlafish1_masks.tiff")
skio.imsave(save_name, masks, check_contrast=False)
