# ogs-data-analysis-tools
A collection of tools for fetching and analyzing user data from OGS

This repository houses various small utilities (mostly consisting of Python notebooks) for fetching and analyzing user data from the [Online Go Server (OGS)](https://online-go.com/).
Each utility is housed in its own top-level folder.
To build, download the entire folder for a given utility.
At this time the scope of each utility here is too small to warrant a full separate repository, which is why they are maintained here.

## Description of individual utilities

* personal_stats:
  * Fetches and stores all of your personal OGS games data.
  * Creates a cleaned version of your OGS games data for use in future statistical/data science applications.
  * Creates dump of all of your OGS games in SGF format.
  * Similar in spirit to the [Got Stats?](https://avavt.github.io/gotstats/#/) tool, but aimed at providing the raw data to the user for use in their own analysis projects.
  * Future work: data analysis and visualization tools using above datasets/game dumps.