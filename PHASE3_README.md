# Phase 3: API and web collection (run and verify)

The existing 90-row IBM capstone dataset and its verified outputs are unchanged.

## Run in PowerShell
From `SpaceX_Capstone_Workspace`:

    python -m pip install --user pandas lxml html5lib beautifulsoup4
    python api_collection.py
    python web_scraping.py

Outputs are written to `collection_outputs/`. The API endpoint or web page may be unavailable or changed. Check terminal output and CSVs; do not claim success unless they exist.

## Important dataset distinction
`dataset_part_2.csv` is the historical IBM training dataset used for the existing 90-launch charts and ML model. The API and web-scraped records are separate sources and may have different row counts or dates. Do not merge them without schema mapping and validation.

## Coursera integrity
Review, execute, understand, and modify the scripts yourself. The final presentation should only claim analyses you actually ran and verified. GitHub publication and final PDF submission remain separate steps.
