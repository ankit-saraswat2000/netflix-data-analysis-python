# Netflix Data Analysis Using Python — Auspify Internship

## Project coverage
This project implements all six tasks listed in the supplied internship PDF:
1. Netflix data cleaning and preparation
2. Movie vs TV Show content-type analysis
3. Country-wise content analysis
4. Release-year trend analysis
5. Rating and genre analysis
6. Business insights report

## Dataset
The supplied `Dataset.csv` contains Netflix catalogue records. The cleaned dataset is saved as `netflix_cleaned.csv`.
Some fields such as director, country, rating, duration and genres may be missing in the source. These are labelled `Not Specified` for analysis; `date_added` remains blank if it cannot be parsed.

## Run the code
1. Install Python 3.10+.
2. Install dependencies: `pip install pandas matplotlib`
3. Keep `Dataset.csv` in the same folder as `netflix_analysis.py`.
4. Run: `python netflix_analysis.py`
5. Results are written to the `outputs/` folder.

## Important counting note
Country and genre columns can contain multiple comma-separated values. For country and genre ranking, each title is split into its country/genre entries. Therefore these rankings count title-country or title-genre entries, not unique titles by one exclusive country/genre.

## Submission checklist
- `netflix_analysis.py` — reproducible source code
- `netflix_cleaned.csv` — cleaned dataset
- `charts/` — generated chart images
- summary CSV tables
- `Netflix_Analysis_Report.pdf` — written report
- `Dataset.csv` — original input file, included for reproducibility
