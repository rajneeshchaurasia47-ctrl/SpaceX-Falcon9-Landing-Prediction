# SpaceX Capstone — reproducible analysis starter

This is a starter for performing your **own** IBM SpaceX Falcon 9 analysis, not a completed Coursera submission. It does not claim that the API, scraping, Folium, or Dash assignments have been completed.

## Run

```bash
pip install -r requirements.txt
python run_analysis.py
```

The script downloads IBM's public `dataset_part_2.csv` once (or reads a copy placed in this folder). It generates **real** data summaries, EDA figures, SQL query results, and a logistic regression baseline in `outputs/`. Verify the results before presenting them.

## Important limits

- Data represents the historical IBM course sample, not current SpaceX launches.
- Model evaluation is a simple stratified holdout; small sample sizes cause uncertainty.
- Data collection via API and scraping, Folium, and Dash must be completed and documented separately.
- Do not claim that this starter project is your completed capstone submission.

Dataset reference: IBM Skills Network `IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv`.
