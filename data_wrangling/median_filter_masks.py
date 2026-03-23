#!/usr/bin/env python
# coding: utf-8

"""Smooths out the edges of manually segmented cells. Allows for noise reduction while still preserving edges.
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import os
from os.path import join
from scipy.ndimage import median_filter, grey_dilation,grey_erosion
from skimage.morphology import erosion
from skimage.transform import rescale,resize
import raster_geometry as rg
import sys

mask_path = './fixed_labels/'
img_path = '../'
output_path = './median_filter/'

os.makedirs(output_path, exist_ok=True)

imglist = [i for i in os.listdir(mask_path) if (('.tiff' in i) and ('median' not in i)) ]
print(imglist)

ellipsoid = rg.ellipsoid((2,4,4),semiaxes=(1,2,2))
big_ellipsoid = rg.ellipsoid((4,8,8),semiaxes=(2,4,4))
for maskname in imglist:
    
    mask_3d = io.imread(join(mask_path,maskname))
    sz,sx,sy = mask_3d.shape
    # Calculate median filter of the masks
    
    mask_3d = median_filter(mask_3d,footprint=ellipsoid,output=np.uint8)
    border_mask = grey_dilation(mask_3d,footprint=ellipsoid) != grey_erosion(mask_3d,footprint=ellipsoid)
    mask_3d[border_mask] = 0
    mask_3d = grey_dilation(mask_3d,footprint=ellipsoid)
    #median_3d = erosion(mask_3d,footprint=np.ones((2,4,4)))
    
    
    imgname=maskname.replace(".tiff","_median.tiff")
    io.imsave(join(output_path, imgname), mask_3d, check_contrast=False)
        
