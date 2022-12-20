# OGS Personal Stats Utilities
* Fetches and stores OGS games data for a given player.
* Creates a cleaned version of fetched games data for use in future statistical/data science applications.
* Creates dump of player's games in SGF format. List of games can be pre-filtered.
* Similar in spirit to the [Got Stats?](https://avavt.github.io/gotstats/#/) tool, but aimed at providing the raw data to the user for use in their own analysis projects.
* Some pre-analyzed professional games (SGFs, JSONs, cleaned JSONs) are provided in the `./output/pro/` directory if you want to play around with datasets immediately. Gratitude goes to to [Baduk Movies](https://badukmovies.com/pro_games) for providing a database of pro games for the public domain.

## Usage

### Requirements

* An OGS account. You can sign up for an account [here](https://online-go.com/).

### **(Required: do this first)** OAuth token
1. Create an OGS OAuth 2.0 application. You can create one [here](https://online-go.com/oauth2/applications/). Copy the client id and client secret fields before saving. For the settings you can set Client type - public, Authorization Grant Type - password.
2. Replace the corresponding terms in the file `keys.txt` with your client id, client secret, OGS username, and OGS password. Keep the double quotes. These will be needed to create an OAuth key which is needed to make requests to the OGS API.
    
### Fetching and cleaning user games data
1. **(This step must be performed before all others.)** Fetching stats:
    1. Open `stats_dump.ipynb`.
    2. Modify the player ID you wish to fetch stats for.
    2. Run all cells, and wait for the API requests to conclude. This may take several minutes.
    3. Confirm creation of output file.
2. Cleaning:
    1. Open `stats_cleanup.ipynb`.
    2. Modify the player ID to the same player ID from step 1.
    3. (Optional) Modify code cell 4 if you wish to include specific columns in the dataset that are dropped by default. If you do this, you may want to also modify the subsequent cells to do cleanup on your included columns.
    3. Run all cells.
    4. Confirm creation of output file. This is a cleaned JSON dataset for use in further statistical/data analysis projects.
3. Fetching games:
    1. Open `games_dump.ipynb`.
    2. Modify the player ID to the same player ID from step 1.
    3. (Optional) Choose an alternative database of games to fetch. Default databases are made in steps 1 and 2.
    3. Run all cells, and wait for the API requests to conclude. This may take several minutes.
    4. Confirm creation of output files.

### Analyzing games

**Dependencies:**
* [KataGo](https://github.com/lightvector/KataGo)
* [analyze-sgf](https://github.com/9beach/analyze-sgf)

1. Producing analysis for single game:
    1. Open `game_analysis.ipynb`.
    2. Modify id information to point to correct SGF.
    3. Run all cells. This step will usually take a long time.
    4. Confirm creation of output files:
        * an SGF with analysis added named `<filename>-analyzed.sgf`.
        * a JSON containing the analysis data named `<filename>.json`.
        * a JSON containing a cleaned version of the analysis data named `<filename>_clean.json`.
2. Producing analysis for multiple games:
    1. Open `game_analysis_mass.ipynb`.
    2. Create the directory `./output/<player_id>/sgf_for_analysis/`; if it already exists, empty it.
    3. Place SGFs for analysis in said directory.
    4. Modify path and ID information in notebook.
    3. Run all cells. This step will usually take a long time.
    4. Confirm creation of output files within `./output/<player_id>/sgf_for_analysis/`:
        * an SGF with analysis added named `<filename>-analyzed.sgf`.
        * a JSON containing the analysis data named `<filename>.json`.
        * a JSON containing a cleaned version of the analysis data named `<filename>_clean.json`.

### Game analytics:

1. Sharpness (`sharpness.ipynb`):
    * Measures the sharpness of each move (whether many or only a few options are viable in a given position)
    * Provides summary statistic for player performance in sharp board states