import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# works for
# python 3.6
# pandas 0.25
# matplotlib 3.1.1

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import pytz
from git import Repo
import shutil
import tempfile
import os.path

import sunpy_paper

fig, axes = plt.subplots(1, 3, figsize=(15, 5.0))


datafile_url = os.path.join(sunpy_paper.data_dir, "loc_vs_time.csv")
data = pd.read_csv(datafile_url, parse_dates=True, index_col=0, comment="#")
x = pd.to_datetime(data.index, utc=True)
y1 = data["code"].values / 10000.0
y2 = data["comment"].values / 10000.0
axes[0].plot(x, y1, label="code", color="black", linestyle="-")
axes[0].plot(x, y2, label="comment", color="black", linestyle="--")

axes[0].set_ylabel("Lines (thousands)")
axes[0].set_xlabel("Year")
axes[0].set_ylim(0, 3.5)
axes[0].legend(loc=2, frameon=False)
axes[0].minorticks_off()

axes[0].xaxis.set_tick_params(labelrotation=45)
# add vertical lines for the releases
sunpy_paper.add_releases_vs_time(axes[0])


dirpath = tempfile.mkdtemp()
# grab a clean cloned repo from github
repo = Repo.clone_from("git@github.com:sunpy/sunpy.git", dirpath)

# make sure you are on the 1.0 branch
g = repo.git
g.checkout("v1.0.0")

commits = list(repo.iter_commits("master"))
commit_datetime = [
    pd.to_datetime(c.committed_datetime.astimezone(pytz.utc)) for c in commits
]
authors = [f"{c.author.name} <{c.author.email}>" for c in commits]
mailmap = sunpy_paper.get_author_transform_mapping(repo)
mapped_authors = [mailmap.get(a.strip().lower(), a.strip().lower()) for a in authors]
author_names = [c.author.name.lower() for c in commits]
author_emails = [c.author.email for c in commits]
data = pd.DataFrame(data={"author": mapped_authors}, index=commit_datetime)

temp = data["author"].resample("M").apply(set)
# drop the last row since data is not full
temp.drop(temp.tail(1).index, inplace=True)

x = pd.DataFrame(data={"set": temp.values}, index=temp.index)
x["count"] = [len(v) for v in x["set"].values]


# author commits
# fig, ax1 = plt.subplots()
# x["count"].plot(ls="steps")
# plt.ylabel("Committers per month")

# sunpy_paper.add_releases_vs_time(ax1)
# plt.savefig("committers_per_month_vs_time.pdf")

# now plot cumulative authors as a function of time
a = set()
result = []
for i in range(len(x["set"].values)):
    these_authors = x["set"].values[0:i]
    a = []
    for this_set in these_authors:
        a += list(this_set)
    result.append(len(set(a)))
cum_authors = pd.Series(data=result, index=temp.index)
cum_authors.plot(color="black", linestyle="-", ax=axes[1])
axes[1].set_ylabel("Cumulative Contributors")
axes[1].set_xlabel("Year")
axes[1].minorticks_off()
axes[1].xaxis.set_tick_params(labelrotation=45)

sunpy_paper.add_releases_vs_time(axes[1])

# now create a plot of the number of commits versus the number of committers

author_count = data.groupby("author").apply(lambda x: len(x))
# author_count.sort_values('author', inplace=True)
bins = np.logspace(np.log10(1), np.log10(10000), 20)
author_count.hist(ax=axes[2], bins=bins, color="grey", lw=0, grid=False)
vals, bins = np.histogram(author_count.values, bins=bins)

bin_centers = np.log10(bins) + (np.log10(bins[1]) - np.log10(bins[0])) / 2.0
x = bin_centers[:-1]
y = np.log10(vals)
result = np.polyfit(x[:-4], y[:-4], deg=1)
axes[2].plot(
    10 ** x[:-2],
    10 ** (result[0] * x[:-2] + result[1]),
    label="$N^{" + "{0:0.2f}".format(result[0]) + "}$",
    color="black",
    linestyle="-",
)
axes[2].legend(frameon=False, fontsize="xx-large")
axes[2].set_yscale("log")
axes[2].set_xscale("log")
xticks = [1, 10, 100, 1000, 10000]
axes[2].set_xticks(xticks)
axes[2].set_xticklabels([str(tick) for tick in xticks])

yticks = [1, 10, 100]
axes[2].set_yticks(xticks)
axes[2].set_yticklabels([str(tick) for tick in yticks])
axes[2].set_ylim(0.8, 100)
axes[2].set_xlim(1, 20000)

axes[2].set_ylabel("Number of Contributors")
axes[2].set_xlabel("Number of Commits")

axes[2].set_title("")
plt.savefig("dev_meta.pdf")

shutil.rmtree(dirpath)
