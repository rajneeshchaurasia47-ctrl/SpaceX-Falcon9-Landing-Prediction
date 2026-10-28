"""Collect public SpaceX launch records from the SpaceX REST API.
This is supplementary live API evidence, not a replacement for the IBM 90-row dataset.
"""
from pathlib import Path
import json
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'collection_outputs'
OUT.mkdir(exist_ok=True)
URL = 'https://api.spacexdata.com/v4/launches'
request = urllib.request.Request(URL, headers={'User-Agent':'SpaceXCapstoneEducationalProject/1.0'})
with urllib.request.urlopen(request, timeout=40) as response:
    launches = json.load(response)
rows = []
for item in launches:
    rows.append({
        'id': item.get('id'),
        'name': item.get('name'),
        'date_utc': item.get('date_utc'),
        'flight_number': item.get('flight_number'),
        'success': item.get('success'),
        'rocket_id': item.get('rocket'),
        'launchpad_id': item.get('launchpad'),
        'payload_count': len(item.get('payloads') or []),
    })
df = pd.DataFrame(rows)
df.to_csv(OUT / 'spacex_api_launches.csv', index=False)
(OUT / 'api_collection_summary.txt').write_text(
    f'Endpoint: {URL}\nRows collected: {len(df)}\n'
    f'Date range: {df.date_utc.min()} to {df.date_utc.max()}\n'
    'Source: SpaceX v4 public launches API. This is a separate live dataset.\n',
    encoding='utf-8')
print('Saved:', OUT / 'spacex_api_launches.csv', '| Rows:', len(df))
