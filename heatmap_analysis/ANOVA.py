import csv
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import numpy as np

"""
Runs an ANOVA on mean intensity per neuromast results
  Inputs: 
    CSV file containing the mean intensity per neuromast,
    this is tailored to the three treatment groups of WT, 40LY, and 400LY
  Outputs:
    ANOVA statistics and bar graph
"""


wt = []
ly40 = []
ly400 = []
with open("mean_intensities_with_treatment.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        val = float(row["Mean_Intensity"])
        if row["Treatment"] == "WT":
            wt.append(val)
        elif row["Treatment"] == "40LY":
            ly40.append(val)
        elif row["Treatment"] == "400LY":
            ly400.append(val)

#Calucate f statistics and pvalue
f_stat, p_val = stats.f_oneway(wt, ly40, ly400)
print("ANOVA results:")
print("F-statistic:", f_stat)
print("p-value:", p_val)

data = wt + ly40 + ly400
groups = (["WT"] * len(wt)) + (["40LY"] * len(ly40)) + (["400LY"] * len(ly400))

#Do a tukey hsd since our results were significant
tukey = pairwise_tukeyhsd(endog=data, groups=groups, alpha=0.05)
print("\nTukey HSD results:")
print(tukey)

group_labels = ["WT", "40LY", "400LY"]
group_data = [wt, ly40, ly400]
means = [np.mean(g) for g in group_data]
sds = [np.std(g, ddof=1) for g in group_data]
colors = ["#5DCAA5", "#7F77DD", "#D4537E"]

#plot results
fig, ax = plt.subplots(figsize=(6, 5))
x = np.arange(len(group_labels))
bars = ax.bar(x, means, yerr=sds, capsize=5, color=colors, edgecolor="black", width=0.5)
ax.set_xticks(x)
ax.set_xticklabels(group_labels)
ax.set_ylabel("Mean HCR intensity (per neuromast)")
ax.set_title("Delta-D expression by treatment group")
ax.set_ylim(0, max(means) + max(sds) + 0.15)

# Significance brackets from Tukey results
tukey_results = tukey.summary().data[1:]  # skip header
def add_bracket(ax, x1, x2, y, label):
    ax.plot([x1, x1, x2, x2], [y, y+0.01, y+0.01, y], lw=1, color="black")
    ax.text((x1+x2)/2, y+0.015, label, ha="center", va="bottom", fontsize=10)

bracket_y = max(means) + max(sds) + 0.02
for row in tukey_results:
    g1, g2, _, p, _, _, reject = row
    label = "**" if p < 0.01 else ("*" if p < 0.05 else "ns")
    i1 = group_labels.index(g1)
    i2 = group_labels.index(g2)
    add_bracket(ax, i1, i2, bracket_y, label)
    bracket_y += 0.055

plt.tight_layout()
plt.savefig("deltaD_expression_bargraph.png", dpi=300)
plt.show()
