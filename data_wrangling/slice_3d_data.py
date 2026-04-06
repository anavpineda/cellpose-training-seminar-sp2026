#!/usr/bin/env python
# coding: utf-8
#%%
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from cellpose import models
import os
from os.path import join
from skimage.util import invert
from skimage.transform import rescale,resize
from skimage.exposure import rescale_intensity
import sys
from natsort import natsorted

"""Slice 3D Z-stack. Loads matching trios of mask + nuclei + membrane 3D tiff stacks.
Slices in 3 orientations to maximize training data: XY XZ YZ + their mask pairs
Necessary for Cellpose training
Inputs:
    mask_path: manually segmented masks
    img_path: raw tiff files of nuceli and membrane
Output:
    slice_path: path to new slices folder"""


# Manually created masks, median filter should be added to reduce noise
mask_path = '/masks'

# Raw nuclei and membrane images
img_path = '/raw'

#Output path containing all the slices, will be very large
slices_path = '/Slices'

# Edit to match local naming
masklist = natsorted([i for i in os.listdir(mask_path) if '_median.tiff' in i])
nuclei_list =natsorted([i for i in os.listdir(img_path) if (('membrane' in i) and ('.tiff' in i))])
membrane_list =natsorted([i for i in os.listdir(img_path) if (('nuclei' in i) and ('.tiff' in i))])

print(masklist)
print(nuclei_list)
print(membrane_list)

nfiles = len(masklist)

#Slice data
for file_n in range(nfiles):
    
    maskname = masklist[file_n]
    mask_3d = io.imread(join(mask_path,maskname))
    sz,sx,sy = mask_3d.shape
    
    mask_3d_rescaled = rescale(mask_3d,scale=(2.5,1,1),order=0,preserve_range=True).astype(np.uint16)

    #imgname=maskname.replace("predictions_CellPose_2_Manual_median.tiff","combined.tiff")
    nuclei_img = nuclei_list[file_n]
    nuclei_3d= rescale_intensity(io.imread(join(img_path,nuclei_img)),out_range='uint16')
    
    membrane_img = membrane_list[file_n]
    membrane_3d= rescale_intensity(invert(io.imread(join(img_path,membrane_img))),out_range='uint16')
    
    print(mask_3d.shape, nuclei_3d.shape, membrane_3d.shape)
    
    nuclei_3d_rescaled = rescale(nuclei_3d,scale=(2.5,1,1),order=1,preserve_range=True)
    membrane_3d_rescaled = rescale(membrane_3d,scale=(2.5,1,1),order=1,preserve_range=True)

    print(mask_3d_rescaled.shape, nuclei_3d_rescaled.shape, membrane_3d_rescaled.shape)
    
    sz,sy,sx = mask_3d.shape
    
    for k in range(sz):
        if np.sum(mask_3d[k,:,:]>0):
            slice = np.zeros((3,sy,sx),dtype=np.uint16)
            slice[0,:,:] = membrane_3d[k,:,:]
            slice[1,:,:] = nuclei_3d[k,:,:]
            print(slice.shape)
            
            slicename = nuclei_img.replace('.tiff', f'_{k:03}.tiff')
            io.imsave(join(slices_path,slicename),slice,check_contrast=False)
            maskslicename = nuclei_img.replace('.tiff', f'_{k:03}_masks.tiff')
            io.imsave(join(slices_path,maskslicename),mask_3d[k,:,:],check_contrast=False)
            print(maskslicename)
    
    rsz,rsy,rsx = mask_3d_rescaled.shape

    for j in range(0,rsy,5):
        if np.sum(mask_3d_rescaled[:,j,:]>0):
            slice = np.zeros((3,rsz,sx),dtype=np.uint16)
            slice[0,:,:] = membrane_3d_rescaled[:,j,:]
            slice[1,:,:] = nuclei_3d_rescaled[:,j,:]
            print(slice.shape)

            slicename = nuclei_img.replace('.tiff', f'_xz_{j:03}.tiff')           
            io.imsave(join(slices_path,slicename),slice,check_contrast=False)
            maskslicename = nuclei_img.replace('.tiff', f'_xz_{j:03}_masks.tiff')
            io.imsave(join(slices_path,maskslicename),mask_3d_rescaled[:,j,:],check_contrast=False)
            print(maskslicename)

    for j in range(0,rsy,5):
            if np.sum(mask_3d_rescaled[:,:,j]>0):
                slice = np.zeros((3,rsz,sy),dtype=np.uint16)
                slice[0,:,:] = membrane_3d_rescaled[:,:,j]
                slice[1,:,:] = nuclei_3d_rescaled[:,:,j]
                print(slice.shape)

                slicename = nuclei_img.replace('.tiff', f'_yz_{j:03}.tiff')           
                io.imsave(join(slices_path,slicename),slice,check_contrast=False)
                maskslicename = nuclei_img.replace('.tiff', f'_yz_{j:03}_masks.tiff')
                io.imsave(join(slices_path,maskslicename),mask_3d_rescaled[:,:,j],check_contrast=False)
                print(maskslicename)
# %%
