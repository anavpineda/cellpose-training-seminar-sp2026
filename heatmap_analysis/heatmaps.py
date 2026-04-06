import os
import csv
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
from scipy import ndimage

"""Create heatmaps and save intensity statistics to a CSV
    Inputs: 
      labels:Segmentation labels 
      flourescence_path: HCR visualization results
    Outputs:
      CSV of pixel intensity
      TIFF of visualized heatmap
    """

# Read the input files
labels = tiff.imread('/overlap_manual/')
fluorescence_path = ('/dld_1.tiff')
fluorescence = tiff.imread(fluorescence_path)

output_path = '/heatmaps'

# Get middle slice for visualization
if len(labels.shape) == 3:
    mid_slice = labels.shape[0] // 2
    labels_2d = labels[mid_slice]
    print(f"Using middle slice for visualization: {mid_slice}")
else:
    labels_2d = labels
    mid_slice = None

if len(fluorescence.shape) == 3:
    fluorescence_2d = np.max(fluorescence, axis=0)  # MIP for visualization
else:
    fluorescence_2d = fluorescence

# Get unique labels (excluding background which is typically 0)
unique_labels = np.unique(labels)
unique_labels = unique_labels[unique_labels != 0]  # Remove background
print(f"Number of unique labels: {len(unique_labels)}")

# Create a dictionary to store mean intensities for each label
label_intensities = {}

# Calculate mean fluorescence intensity for each labeled region
# Use original 3D fluorescence data if available
fluorescence_for_calc = fluorescence

for label_id in unique_labels:
    # Create mask for current label
    if len(labels.shape) == 3 and len(fluorescence_for_calc.shape) == 3:
        # Both 3D - broadcast mask across all slices
        mask = (labels == label_id)
    elif len(labels.shape) == 2 and len(fluorescence_for_calc.shape) == 3:
        # 2D labels with 3D fluorescence - broadcast the mask
        mask = np.broadcast_to((labels == label_id)[np.newaxis, :, :],
                               fluorescence_for_calc.shape)
    else:
        mask = (labels == label_id)

    # Get fluorescence values within the mask
    fluorescence_values = fluorescence_for_calc[mask]

    # Calculate mean intensity
    mean_intensity = np.mean(fluorescence_values)
    label_intensities[label_id] = mean_intensity

print(f"Intensity range: {min(label_intensities.values()):.2f} - {max(label_intensities.values()):.2f}")

# Create 3D heatmap by replacing each label with its mean intensity
# Normalize between 0 and 1
min_intensity = min(label_intensities.values())
max_intensity = max(label_intensities.values())
intensity_range = max_intensity - min_intensity

# Create 3D heatmap (same shape as original labels)
heatmap_3d = np.zeros_like(labels, dtype=np.float32)

for label_id, intensity in label_intensities.items():
    # Normalize: (value - min) / (max - min) gives range [0, 1]
    if intensity_range > 0:
        normalized_intensity = (intensity - min_intensity) / intensity_range
    else:
        normalized_intensity = 0.0
    heatmap_3d[labels == label_id] = normalized_intensity


print(f"Normalized heatmap range: {heatmap_3d[heatmap_3d > 0].min():.4f} - {heatmap_3d.max():.4f}")

# Extract the base name without extension
base_name = os.path.splitext(os.path.basename(fluorescence_path))[0]

# Save the 3D heatmap as TIFF
heatmap_filename = os.path.join(output_path, f'{base_name}_fluorescence_heatmap.tiff')
print(f"Saving 3D heatmap as {heatmap_filename}...")
tiff.imwrite(heatmap_filename, heatmap_3d.astype(np.float32))
print(f"Saved 3D heatmap with shape: {heatmap_3d.shape}")

# Save intensity statistics to CSV
csv_filename = os.path.join(output_path,f'{base_name}_label_intensities.csv')
print(f"Saving intensity statistics as {csv_filename}...")
with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Label_ID', 'Mean_Fluorescence_Intensity', 'Normalized_Intensity_0_1'])
    for label_id in sorted(label_intensities.keys()):
        intensity = label_intensities[label_id]
        if intensity_range > 0:
            normalized = (intensity - min_intensity) / intensity_range
        else:
            normalized = 0.0
        writer.writerow([label_id, intensity, normalized])

print("\nComplete! Files saved:")
print(f"  - {heatmap_filename} (3D)")
print(f"  - {csv_filename}")

print("\nComplete! Files saved:")
print("  - fluorescence_heatmap.tiff (3D)")
print("  - label_intensities.csv")
print(f"\nOriginal intensity range: {min_intensity:.2f} - {max_intensity:.2f}")
print(f"Normalized intensity range: 0.00 - 1.00")

plt.show()

