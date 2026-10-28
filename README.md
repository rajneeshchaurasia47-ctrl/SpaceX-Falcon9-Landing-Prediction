# SpaceX Falcon 9 First-Stage Landing Prediction

IBM Applied Data Science Capstone: reproducible historical analysis of 90 labelled Falcon 9 launches. This repository includes **completed local analysis** and separately documented **incomplete remote collection workflows**.

## Verified results
- 90 launches, 60 successful landings (66.7%).
- Site-level and orbit-level EDA visualizations: `outputs/site_success.png`, `outputs/orbit_success.png`, `outputs/flight_payload.png`.
- SQLite query results: `outputs/sql_results.txt` and `outputs/spacex.db`.
- Original logistic-regression test accuracy: 18/23 = 78.26%; confusion matrix `[[3,5],[0,15]]`. This model misses 5/8 failures.
- Four-classifier comparison: `model_comparison.py` runs Logistic Regression, SVM (RBF), Decision Tree, and KNN using training-only preprocessing and five-fold training cross-validation. Observed KNN test accuracy is 19/23 = 82.61%, but misses 4/8 failures.
- Interactive local dashboard code: `interactive/build_spacex_interactive.py`. Folium HTML at `interactive/interactive_outputs/launch_sites_map.html`; original basemap rendering was restricted.

## Run
```bash
python -m pip install -r requirements.txt
python run_analysis.py
python model_comparison.py
python -m pip install -r interactive/requirements_interactive.txt
python interactive/build_spacex_interactive.py
```

## Notebooks and evidence
- `notebooks/01_Data_Provenance_and_Wrangling.ipynb` — analysis dataset and preprocessing.
- `notebooks/02_EDA_and_SQL.ipynb` — SQL and visualization.
- `notebooks/03_Folium_Map.ipynb` — map methodology.
- `notebooks/04_Predictive_Classification.ipynb` — model methodology.
- `model_comparison.py` — actual reproducible four-model comparison (not all notebook output cells are executed in the repository).

## Collection and source limitations
- The study uses the IBM-provided local `dataset_part_2.csv`. It does **not** demonstrate successful extraction of the same dataset via SpaceX API or Wikipedia.
- `api_collection.py` and `web_scraping.py` are attempts; previous requests failed (HTTP 522/525 and HTTP 403). Do not describe them as successfully executed.
- Archived IBM lab API JSON: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json
- Historical Wikipedia snapshot used in IBM scraping lab: https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922
- Historical IBM SQL lab table (101 rows, **separate** from the 90-row ML data): https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv

Results are descriptive and educational, not flight-safety predictions.