"""Educational web scraping of a public HTML table of Falcon 9 launches.
The page structure may change. Observe site terms and robots policy.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'collection_outputs'
OUT.mkdir(exist_ok=True)
URL = 'https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches'
print('Reading publicly available HTML tables from:', URL)
tables = pd.read_html(URL)
summary = []
for i, table in enumerate(tables):
    summary.append({'table_index': i, 'rows': len(table), 'columns': len(table.columns),
                    'column_names': ' | '.join(map(str, table.columns))[:400]})
report = pd.DataFrame(summary)
report.to_csv(OUT / 'web_table_inventory.csv', index=False)
if not tables:
    raise RuntimeError('No HTML tables found')
# Store the largest table as raw evidence; do not pretend it is cleaned launch data.
largest = max(tables, key=len)
largest.to_csv(OUT / 'web_largest_raw_table.csv', index=False)
print('Saved HTML table inventory and largest raw table. Inspect before cleaning.')
