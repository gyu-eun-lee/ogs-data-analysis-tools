# OGS Personal Stats Utilities
* Fetches and stores all of your personal OGS games data.
* Creates a cleaned version of your OGS games data for use in future statistical/data science applications.
* Creates dump of all of your OGS games in SGF format.
* Similar in spirit to the [Got Stats?](https://avavt.github.io/gotstats/#/) tool, but aimed at providing the raw data to the user for use in their own analysis projects.

## Usage

### Requirements

* An OGS account. You can sign up for an account [here](https://online-go.com/).

### **(Required: do this first)** OAuth token
1. Create an OGS OAuth 2.0 application. You can create one [here](https://online-go.com/oauth2/applications/). Copy the client id and client secret fields before saving.
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
    3. Run all cells, and wait for the API requests to conclude. This may take several minutes.
    4. Confirm creation of output files.