from git import Repo
import datetime
import shutil
import tempfile
import os.path
import pytz
import pandas as pd


import .figures/sunpy_paper

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

number_unique_authors = len(set(mapped_authors))
print(f"There are {number_unique_authors} unique authors")

dev_days = (datetime.datetime(2019, 6, 1) - datetime.datetime(2011, 4, 15)).days

new_contributors_per_month = number_unique_authors / dev_days * 30.42
print(f"There are {new_contributors_per_month} new contributors added every month.")

data = pd.DataFrame(data={"author": mapped_authors}, index=commit_datetime)

total_lines_of_code = 48427
lines_of_code_per_day = total_lines_of_code / dev_days
print(f"{lines_of_code_per_day} lines of code added per day")

author_count = data.groupby("author").apply(lambda x: len(x))
number_of_top_contributors = 10
percent_of_commits = author_count.sort_values()[-number_of_top_contributors:].sum() / author_count.sum()
print(f'The top {number_of_top_contributors} contributors generated {percent_of_commits} of commits')
