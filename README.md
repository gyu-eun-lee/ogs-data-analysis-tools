# ogs-data-analysis-tools
A collection of tools for fetching and analyzing user data from OGS

This repository houses various small utilities (mostly consisting of Python notebooks) for fetching and analyzing user data from the [Online Go Server (OGS)](https://online-go.com/).
Each utility is housed in its own top-level folder.
To build, download the entire folder for a given utility.
At this time the scope of each utility here is too small to warrant a full separate repository, which is why they are maintained here.

## Description of individual utilities

* player_data_tools:
    * Tools for dumping and analyzing individual player data.
    * Dump datasets of all of a player's game information (ranks, outcomes, etc.)
    * Basic cleaning of datasets for use in subsequent statistics/data analysis applications
    * Dump player's games in JSON and SGF formats
        * Games can be pre-filtered using raw and cleaned datasets
    * Use KataGo to analyze full games, including multiple games at once
        * Also produces clean Pandas-ready JSON files with the analysis data
        * A few pre-analyzed professional games are provided. 2000 visits per root.
    * Analytics using above tools
        * Sharpness coefficient: Measure the sharpness of each move