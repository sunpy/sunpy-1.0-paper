"""The following file contains generic functions to produce the plots in the sunpy paper."""
import os
import seaborn
import matplotlib
from pathlib import Path
import pandas as pd

import sunpy

sunpy_releases = {
    "1.0": "2019/06/01",
    ".9": "2018/04/22",
    ".8": "2017/08/17",
    ".7": "2016/05/24",
    ".6": "2015/07/21",
    ".5": "2014/06/13",
    ".4": "2014/02/14",
    ".3": "2013/08/30",
    ".2": "2012/11/26",
    ".1": "2011/09/28",
}

data_dir = Path(os.path.join(Path(__file__).parents[1], "data"))


def get_author_transform_mapping(repo):
    """
    Read the mailmap into a `dict` to be used to transform authors.

    Parameters
    ----------
    repo : `git.Repo`
    """

    mailmap_file = Path(repo.working_tree_dir) / ".mailmap"

    if not mailmap_file.exists():
        raise ValueError("This repo does not have a mailmap")

    with open(mailmap_file) as fd:
        mailmap_lines = fd.readlines()

    for i, line in enumerate(mailmap_lines):
        line = line.strip().lower()
        split = line.find("> ") + 1
        mailmap_lines[i] = (line[:split].strip(), line[split + 1 :].strip())[::-1]

    return dict(mailmap_lines)


def get_author_email_list(repo):
    """
    Read the mailmap and return a list of all author emails.

    Parameters
    ----------
    repo : `git.Repo`
    """
    mailmap_dict = get_author_transform_mapping(repo)
    all_emails = set([mailmap_dict[key].split("<")[1][0:-1] for key in mailmap_dict])
    # remove emails with address users.noreply.github.com
    all_good_emails = [
        this_email for this_email in all_emails if "noreply" not in this_email
    ]
    return all_good_emails


def add_releases_vs_time(ax1):
    """Adds vertical lines to a plot as a function of time with the sunpy release dates."""
    release_times = [pd.to_datetime(s) for s in sunpy_releases.values()]
    _, _, _, ymax = ax1.axis()
    ax2 = ax1.twiny()
    ax2.plot(release_times, [ymax - 1] * len(release_times), ".", alpha=0)
    ax2.set_xticks(release_times)
    ax2.set_xticklabels(sunpy_releases.keys())
    ax2.minorticks_off()
    ax2.set_xlabel("SunPy Releases")
    # for this_release in release_times:
    #    ax2.axvline(this_release, color="black", linestyle="..", linewidth=0.1)
