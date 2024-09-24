# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
#     "pandas",
#     "seaborn",
# ]
# ///
from __future__ import annotations

import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Specify the directories you want to analyze
DIRECTORIES_TO_ANALYZE = [
    "core",
    "db",
    "forms",
    "http",
    "newforms",
    "oldforms",
    "template",
    "views",
    "utils",
]

# Specify the contrib modules you want to analyze
CONTRIB_MODULES_TO_ANALYZE = [
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    # Add or remove contrib modules as needed
]


def get_commit_counts(repo_path):
    cmd = f"git -C {repo_path} log --format=%ad --name-only --date=short"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    lines = result.stdout.strip().split("\n")

    commit_data = []
    current_date = None
    for line in lines:
        line = line.strip()
        if line:
            try:
                datetime.strptime(line, "%Y-%m-%d")
                current_date = line
            except ValueError:
                if current_date and line.startswith("django/"):
                    parts = line.split("/")
                    if len(parts) > 2:
                        if parts[1] in DIRECTORIES_TO_ANALYZE:
                            commit_data.append((current_date, parts[1]))
                        elif (
                            parts[1] == "contrib"
                            and len(parts) > 3
                            and parts[2] in CONTRIB_MODULES_TO_ANALYZE
                        ):
                            commit_data.append((current_date, f"contrib.{parts[2]}"))

    return pd.DataFrame(commit_data, columns=["date", "directory"])


# Get the current working directory
cwd = Path.cwd()

# Create a temporary directory and collect data
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Clone Django repository
    django_repo_url = "https://github.com/django/django.git"
    print(f"Cloning Django repository from {django_repo_url}")
    subprocess.run(["git", "clone", django_repo_url, temp_path], check=True)

    # Get commit counts for the specified Django directories
    print("Getting commit counts...")
    df = get_commit_counts(temp_path)

    if df.empty:
        print(
            "No commit data found. Please check the repository structure and specified directories."
        )
        exit(1)

    # Process and group the data by year and directory
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["year"] = df["date"].dt.year
    df = df.groupby(["year", "directory"]).size().reset_index(name="count")
    df = df.sort_values(["year", "directory"])

    # Get unique directories
    directories = sorted(df["directory"].unique().tolist())

    # Create a pivot table for heatmap and total counts
    pivot_df = df.pivot(index="directory", columns="year", values="count").fillna(0)
    pivot_df = pivot_df.sort_index()  # Sort alphabetically

    # Calculate total commits for each module
    pivot_df["Total"] = pivot_df.sum(axis=1)

    # Remove the 'Total' column for the heatmap
    heatmap_df = pivot_df.drop("Total", axis=1)

# Get the overall year range
start_year = df["year"].min()
end_year = df["year"].max()

print(f"Analysis covers commits from {start_year} to {end_year}")


# Function to generate heatmap
def generate_heatmap(highlight_forms=False):
    fig, ax = plt.subplots(figsize=(20, 12))
    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt="g",
        cmap="YlOrRd",
        cbar_kws={"label": "Number of Commits"},
        ax=ax,
    )
    ax.set_title(
        f"Yearly Commit Activity Heatmap for Django Modules\n{start_year} to {end_year}"
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Module")

    if highlight_forms:
        forms_index = heatmap_df.index.get_loc("forms")
        rect = patches.Rectangle(
            (0, forms_index), heatmap_df.shape[1], 1, fill=False, edgecolor="red", lw=2
        )
        ax.add_patch(rect)

    plt.tight_layout()
    return fig


# Generate and save the first heatmap
fig1 = generate_heatmap()
fig1.savefig(cwd / "django_commits_heatmap.png", dpi=300, bbox_inches="tight")
plt.close(fig1)

# Generate and save the second heatmap with forms highlighted
fig2 = generate_heatmap(highlight_forms=True)
fig2.savefig(
    cwd / "django_commits_heatmap_forms_highlighted.png", dpi=300, bbox_inches="tight"
)
plt.close(fig2)

print("Heatmaps have been saved in the current working directory.")

# Print commit counts
print("\nCommit counts by module and year:")
print(pivot_df.to_string())

# Print total commits for each module
print("\nTotal commits by module:")
for module, total in pivot_df["Total"].sort_index().items():
    print(f"{module}: {int(total)} commits")
