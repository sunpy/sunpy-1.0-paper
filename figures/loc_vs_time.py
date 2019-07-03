import os
import matplotlib.pyplot as plt

import pandas as pd

import sunpy_paper

datafile_url = os.path.join(sunpy_paper.data_dir, "loc_vs_time.csv")
data = pd.read_csv(datafile_url, parse_dates=True, index_col=0, comment="#")

x = data.index
y1 = data["code"].values / 10000.0
y2 = data["comment"].values / 10000.0

fig, ax1 = plt.subplots(figsize=(5, 5))
ax1.plot(x, y1, label="code", color="black", linestyle="-")
ax1.plot(x, y2, label="comment", color="black", linestyle="--")

plt.ylabel("Lines (thousands)")
plt.ylim(0, 3.5)

plt.legend(loc=2)

# add vertical lines for the releases
sunpy_paper.add_releases_vs_time(ax1)

plt.savefig("fig_loc_vs_time.pdf")
