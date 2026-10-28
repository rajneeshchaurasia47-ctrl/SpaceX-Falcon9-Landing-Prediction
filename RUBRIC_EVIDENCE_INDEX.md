# IBM SpaceX Capstone — 15-point rubric evidence index

This index links the code behind the accompanying final PDF presentation. Historical evidence only. The original remote API and Wikipedia requests did not succeed; attributed archival mirrors are **not** misrepresented as new API or scraping executions.

| Rubric topic | Verified project evidence |
|---|---|
| Public repository | [README](./README.md), Python source, notebooks and 90-row labeled dataset |
| Executive summary / Introduction | Final PDF slides 2–4 |
| API collection | [API collection script](./api_collection.py); [archived source URL](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json); [attributed mirror](./reference_data/dataset_part_1_api_derived_mirror.csv) |
| Web scraping | [Scraping script](./web_scraping.py); [2021 Wikipedia snapshot](https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922); [attributed mirror](./reference_data/spacex_web_scraped_mirror.csv) |
| Data wrangling | [Provenance and wrangling notebook](./notebooks/01_Data_Provenance_and_Wrangling.ipynb); 90 rows, target Class, 26 missing LandingPad |
| EDA and visualization | [EDA / SQL notebook](./notebooks/02_EDA_and_SQL.ipynb); [site success image](./outputs/site_success.png), [orbit success image](./outputs/orbit_success.png), [payload chart](./outputs/flight_payload.png) |
| **All 10 SQL tasks** | [Runnable SQL script](./sql_lab_complete_10_questions.py) and [101-row attributed teaching CSV](./reference_data/Spacex_SQL_101_mirror.csv). Note: 101 records != 90 in ML data. |
| **Folium** | [Marker clusters + success/failure markers + coastline, highway, railway and city distances](./interactive/folium_proximity_complete.py); [existing map HTML](./interactive/interactive_outputs/launch_sites_map.html) |
| **Plotly Dash** | [Complete dropdown + range slider + all-site/selected-site pie and payload scatter](./interactive/dash_pie_scatter_complete.py); [original local app](./interactive/build_spacex_interactive.py) |
| Classification methodology | [Four-algorithm GridSearchCV script](./tuned_model_evaluation.py) and [notebook](./notebooks/04_Predictive_Classification.ipynb) |
| Four classification results | [Verified CSV](./tuned_model_results_verified.csv), Logistic Regression 20/23 correct (86.96%), confusion [[5,3],[0,15]], failure recall 5/8 |
| Conclusion, creativity, innovative insights | Final PDF slides 36–38: error costs, year/site confounding, calibration, chrono validation and failure recall. |

## Source provenance and caveats
The original attempts to fetch SpaceX API / Wikipedia returned network errors. Therefore these sections report intended workflow, genuine failed attempts, and existing attributed archived snapshots, **not successful direct collection**. Actual calculations for plots and models use the 90-row IBM historical sample. SQL questions refer to a different 101-row teaching table. Proximity coordinates are historical course-example points and not an independent geographic nearest-feature survey.

For reproducibility the full four-classifier tuning results in the presentation come from the repository's `tuned_model_evaluation.py` and the provided IBM `dataset_part_2.csv`. Small test sample (23) limits generalizability.