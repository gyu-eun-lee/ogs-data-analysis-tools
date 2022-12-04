# OGS Personal Stats Utilities
* Fetches and stores all of your personal OGS games data.
* Creates a cleaned version of your OGS games data for use in future statistical/data science applications.
* Creates dump of all of your OGS games in SGF format.
* Similar in spirit to the [Got Stats?](https://avavt.github.io/gotstats/#/) tool, but aimed at providing the raw data to the user for use in their own analysis projects.

## Usage

* Using these tools requires the following:
    * An OGS account. You can sign up for an account [here](https://online-go.com/).
    * An OGS OAuth 2.0 application. You can create one [here](https://online-go.com/oauth2/applications/).
    
### Fetching and cleaning user games data
1. Fetching stats:
    1. Open `stats_dump.ipynb`.
    2. Replace the default key info with your own.
    3. Run all cells, and wait for the API requests to conclude. This may take several minutes.
    4. Confirm creation of output file games.json.
2. Cleaning:
    1. Open `stats_cleanup.ipynb`.
    2. (Optional) Modify code cell [3] if you wish to include specific columns in the dataset that are dropped by default. If you do this, you may want to also modify the subsequent cells to do cleanup on your included columns.
    3. Run all cells.
    4. Confirm creation of output file games_clean.json. This is a cleaned JSON dataset for use in further statistical/data analysis projects.
3. Fetching games:
    1. Open `games_dump.ipynb`.
    2. Replace the default key info with your own.
    3. Run all cells, and wait for the API requests to conclude. This may take several minutes.
    4. Confirm creation of JSON files in `./ogsjson` and SGF files in `./ogssgf`.