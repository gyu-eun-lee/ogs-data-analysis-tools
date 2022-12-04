# OGS Personal Stats Utilities
* Fetches a user's own games data from OGS, performs some data cleaning, and outputs a .json file containing the cleaned data for use in later data analysis projects.
* Later this project may contain data analysis tools utilizing the cleaned data.
* Similar in spirit to the [Got Stats?](https://avavt.github.io/gotstats/#/) tool, but aimed at providing the raw data to the user for use in their own analysis projects.

## Usage

* Using these tools requires the following:
    * An OGS account. You can sign up for an account [here](https://online-go.com/).
    * An OGS OAuth 2.0 application. You can create one [here](https://online-go.com/oauth2/applications/).
    
### Fetching and cleaning user games data
1. Fetching:
    1. Open ogs_personal_stats_ipynb.
    2. Replace the default key info with your own.
    3. Run all cells, and wait for the API requests to conclude. This may take several minutes.
    4. Confirm creation of output file games.json.
2. Cleaning:
    1. Open personal_stats_cleanup.ipynb.
    2. (Optional) Modify code cell [3] if you wish to include specific columns in the dataset that are dropped by default. If you do this, you may want to also modify the subsequent cells to do cleanup on your included columns.
    3. Run all cells.
    4. Confirm creation of output file games_clean.json.

You now have a clean .json file containing your games data which can be used in further data analysis projects.