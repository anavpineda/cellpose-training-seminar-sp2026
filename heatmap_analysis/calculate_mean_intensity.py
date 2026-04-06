import pandas as pd
import glob
import os

"""Takes the intensity CSVs from heatmaps.py and calculates the mean intensity for each neuromast to prepare for ANOVA analysis
      Inputs: 
        folder of intensity CSVs from different treatments
      Outputs:
        One CSV file of mean intensity for each neuromast.   
"""

# get all csv files in current directory
files = glob.glob("*.csv")

results = []

for file in files:
    df = pd.read_csv(file)

    # calculate mean normalized intensity
    mean_intensity = df["Normalized_Intensity_0_1"].mean()

    filename = os.path.basename(file)

    # determine treatment from filename
    if filename.startswith("wt"):
        treatment = "WT"
    elif filename.startswith("40ly"):
        treatment = "40LY"
    elif filename.startswith("400ly"):
        treatment = "400LY"
    else:
        treatment = "Unknown"

    results.append({
        "File": filename,
        "Treatment": treatment,
        "Mean_Intensity": mean_intensity
    })

# create dataframe
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="Treatment")

# save output
results_df.to_csv("mean_intensities_with_treatment.csv", index=False)

print(results_df)
