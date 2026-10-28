"""Run the ten IBM SQL capstone tasks against an attributed 101-row historical CSV mirror.
This SQL teaching table is separate from the 90-row binary Class dataset.
Original source: IBM SQL lab Spacex.csv. Mirror attribution: reference_data/README.md
"""
from pathlib import Path
import sqlite3
import pandas as pd

csv_path = Path(__file__).parent / "reference_data" / "Spacex_SQL_101_mirror.csv"
df = pd.read_csv(csv_path)
db = sqlite3.connect(":memory:")
df.to_sql("SPACEXTBL", db, index=False)
queries = {
    "Q1 / unique sites": 'SELECT DISTINCT Launch_Site FROM SPACEXTBL',
    "Q2 / five CCA rows": 'SELECT Date, Launch_Site, Payload FROM SPACEXTBL WHERE Launch_Site LIKE "CCA%" LIMIT 5',
    "Q3 / NASA CRS mass": 'SELECT SUM(PAYLOAD_MASS__KG_) AS mass_kg FROM SPACEXTBL WHERE Customer = "NASA (CRS)"',
    "Q4 / F9 v1.1 average": 'SELECT AVG(PAYLOAD_MASS__KG_) AS mean_mass_kg FROM SPACEXTBL WHERE Booster_Version LIKE "F9 v1.1%"',
    "Q5 / first ground-pad recovery": 'SELECT MIN(Date) AS first_ground_pad FROM SPACEXTBL WHERE "Landing _Outcome" = "Success (ground pad)"',
    "Q6 / drone recovery payload 4-6t": 'SELECT Booster_Version FROM SPACEXTBL WHERE "Landing _Outcome" = "Success (drone ship)" AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000',
    "Q7 / normalized mission outcomes": 'SELECT TRIM(Mission_Outcome) AS outcome, COUNT(*) AS n FROM SPACEXTBL GROUP BY TRIM(Mission_Outcome) ORDER BY n DESC',
    "Q8 / largest payload booster versions": 'SELECT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)',
    "Q9 / 2015 drone failures": 'SELECT Date, Booster_Version, Launch_Site FROM SPACEXTBL WHERE Date LIKE "2015%" AND "Landing _Outcome" = "Failure (drone ship)"',
    "Q10 / outcome ranking by dates": 'SELECT "Landing _Outcome" AS outcome, COUNT(*) AS n FROM SPACEXTBL WHERE Date BETWEEN "2010-06-04" AND "2017-03-20" GROUP BY 1 ORDER BY n DESC'
}
print("CSV rows:", len(df), "| distinct sites:", df.Launch_Site.nunique())
for label, query in queries.items():
    print("\n", label, "\n", query)
    print(pd.read_sql_query(query, db).to_string(index=False))
print("\nWARNING: historical mirror date strings may differ from other SpaceX chronologies.")
