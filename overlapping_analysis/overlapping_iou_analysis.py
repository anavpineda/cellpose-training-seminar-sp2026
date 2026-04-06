import os
import numpy as np
from tifffile import imread
from cellpose import metrics
import matplotlib.pyplot as plt


"""Uses edited cellpose.metric code, found at https://cellpose.readthedocs.io/en/latest/_modules/cellpose/metrics.html
  Inputs: 
  manual_dir: Manual segmentations / noisy manual segmentations
  predicted_dir: Predicted segmentations
  
  Outputs:
    Heatmap of TP, FP and FN counts at AP50 threshold (can be changed to any other threshold)
    Average precision for the dataset
    """

manual_dir = "/overlap_manual"
predicted_dir = "/overlap/predicted"

file_names = sorted(os.listdir(manual_dir))
all_ap = []
tp_list = []
fp_list = []
fn_list = []

# Matches names of each and calculates average precision, true positive, false positive, and false negative for each neuromast
for file_name in os.listdir(manual_dir):

    manual = imread(os.path.join(manual_dir, file_name))
    pred = imread(os.path.join(predicted_dir, file_name))

    ap, tp, fp, fn = metrics.average_precision(
        manual,
        pred,
        threshold=[0.5, 0.75, 0.9]
    )

    all_ap.append(ap)
    tp_list.append(tp[0])
    fp_list.append(fp[0])
    fn_list.append(fn[0])

    print(f"\n{file_name}")
    print(f"AP50: {ap[0]:.3f}, AP75: {ap[1]:.3f}, AP90: {ap[2]:.3f}")
    print(f"TP: {tp}, FP: {fp}, FN: {fn}")

    all_ap.append(ap)

all_ap = np.array(all_ap)
TP_array = np.array(tp_list)
FP_array = np.array(fp_list)
FN_array = np.array(fn_list)


heatmap_data = np.stack([TP_array, FP_array, FN_array], axis=1)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(heatmap_data, cmap='viridis')

# Labels
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['TP', 'FP', 'FN'])
ax.set_yticks(np.arange(len(file_names)))
ax.set_yticklabels(file_names)
plt.setp(ax.get_yticklabels(), rotation=0, ha="right", rotation_mode="anchor")

# Add counts inside heatmap
for i in range(len(file_names)):
    for j in range(3):
        ax.text(j, i, heatmap_data[i, j], ha="center", va="center", color="w")

ax.set_title("Object-Level Detection Heatmap of Images (AP50)")
fig.colorbar(im, ax=ax, label="Counts")
plt.tight_layout()
plt.show()

print("\n=== DATASET AVERAGE ===")
print(f"AP50: {all_ap[:,0].mean():.3f}")
print(f"AP75: {all_ap[:,1].mean():.3f}")
print(f"AP90: {all_ap[:,2].mean():.3f}")


