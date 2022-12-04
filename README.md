# ogs-data-analysis-tools

This repository houses various small utilities (mostly consisting of Python notebooks) for fetching and analyzing user data from the [Online Go Server (OGS)](https://online-go.com/).
Each utility is housed in its own top-level folder.
To build, download the entire folder for a given utility.
At this time the scope of each utility here is too small to warrant a full separate repository, which is why they are maintained here.

## Description of individual utilities

* personal_stats:
  * Fetches a user's own games data from OGS, performs some data cleaning, and outputs a .json file containing the cleaned data for use in later data analysis projects.
  * Later this project may contain data analysis tools utilizing the cleaned data.
  * Similar in spirit to the [Got Stats?](https://avavt.github.io/gotstats/#/) tool, but aimed at providing the raw data to the user for use in their own analysis projects.
