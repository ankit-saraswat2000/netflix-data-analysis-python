"""
Netflix Data Analysis Using Python — Auspify Internship Tasks
Run: python netflix_analysis.py
Input: Dataset.csv (place in the same folder)
Output: cleaned dataset, summary tables, charts, and insights report.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "Dataset.csv"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

for col in ["show_id", "type", "title", "director", "country", "rating", "duration", "listed_in"]:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
df["type"] = df["type"].str.strip().replace({"tv show": "TV Show", "TV SHOW": "TV Show", "Tv Show": "TV Show", "movie": "Movie"})
df["country"] = df["country"].str.replace(r"\\s+", " ", regex=True)
df["rating"] = df["rating"].str.upper().str.strip()
df["listed_in"] = df["listed_in"].str.replace(r"\\s*,\\s*", ", ", regex=True)
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")

df = df.drop_duplicates()
if "show_id" in df.columns:
    df = df.drop_duplicates(subset=["show_id"], keep="first")
for col in ["director", "country", "rating", "duration", "listed_in"]:
    df[col] = df[col].fillna("Not Specified")

df.to_csv(OUT / "netflix_cleaned.csv", index=False, date_format="%Y-%m-%d")

# Task 2: content type distribution
type_counts = df["type"].value_counts()
type_counts.to_csv(OUT / "content_type_summary.csv", header=["count"])

# Task 3: country analysis; split multi-country entries before counting
countries = df.assign(country_item=df["country"].str.split(", ")).explode("country_item")
countries = countries[countries["country_item"] != "Not Specified"]
country_counts = countries["country_item"].value_counts()
country_counts.head(10).to_csv(OUT / "top_10_countries.csv", header=["title_country_entries"])

# Task 4: releases by release year and date-added trend
releases = df.dropna(subset=["release_year"]).groupby("release_year").size().sort_index()
releases.to_csv(OUT / "releases_by_year.csv", header=["titles"])
added = df["date_added"].dropna().dt.year.value_counts().sort_index()
added.to_csv(OUT / "titles_added_by_year.csv", header=["titles"])

# Task 5: ratings and genres
df["rating"].value_counts().to_csv(OUT / "rating_summary.csv", header=["titles"])
genres = df.assign(genre_item=df["listed_in"].str.split(", ")).explode("genre_item")
genres = genres[genres["genre_item"] != "Not Specified"]
genres["genre_item"].value_counts().head(15).to_csv(OUT / "top_15_genres.csv", header=["title_genre_entries"])
pd.crosstab(df["rating"], df["type"]).to_csv(OUT / "rating_by_content_type.csv")

# Charts
def bar(series, title, xlabel, ylabel, filename, horizontal=False, rotation=0):
    plt.figure(figsize=(10, 6))
    if horizontal:
        series.sort_values().plot(kind="barh")
    else:
        series.plot(kind="bar")
        plt.xticks(rotation=rotation, ha="right" if rotation else "center")
    plt.title(title); plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.tight_layout(); plt.savefig(CHARTS / filename, dpi=180, bbox_inches="tight"); plt.close()

bar(type_counts, "Netflix Titles by Content Type", "Content Type", "Titles", "01_content_type.png")
bar(country_counts.head(10), "Top 10 Countries by Netflix Titles", "Country", "Title-country entries", "03_top_countries.png", True)
bar(releases[releases.index >= 2000], "Netflix Titles by Release Year (2000 onward)", "Release Year", "Titles", "04_release_year_trend.png", rotation=75)
bar(df["rating"].value_counts().head(12), "Most Common Content Ratings", "Rating", "Titles", "05_ratings.png", True)
bar(genres["genre_item"].value_counts().head(15), "Top 15 Genres", "Genre", "Title-genre entries", "05_top_genres.png", True)
plt.figure(figsize=(10,6))
pd.crosstab(df["rating"], df["type"]).loc[df["rating"].value_counts().head(10).index].plot(kind="bar", figsize=(10,6))
plt.title("Content Rating by Type (Top Ratings)"); plt.xlabel("Rating"); plt.ylabel("Titles")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig(CHARTS / "05_rating_by_type.png", dpi=180, bbox_inches="tight"); plt.close()
plt.figure(figsize=(10,6)); added.plot(kind="line", marker="o")
plt.title("Netflix Titles Added by Year"); plt.xlabel("Year Added"); plt.ylabel("Titles")
plt.tight_layout(); plt.savefig(CHARTS / "04_added_year_trend.png", dpi=180, bbox_inches="tight"); plt.close()

# Concise data-driven findings
total = len(df)
movie_n = int((df["type"] == "Movie").sum())
tv_n = int((df["type"] == "TV Show").sum())
print(f"Cleaned records: {total}")
print(f"Movies: {movie_n} ({movie_n/total:.1%})")
print(f"TV Shows: {tv_n} ({tv_n/total:.1%})")
print("Top country entries:", country_counts.head(5).to_dict())
print("Top genres:", genres["genre_item"].value_counts().head(5).to_dict())
print("Outputs saved in:", OUT)
