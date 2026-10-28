from pathlib import Path
import sqlite3
import pandas as pd
import folium
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

ROOT = Path(__file__).resolve().parent
DB = ROOT / 'spacex.db'
OUT = ROOT / 'interactive_outputs'
OUT.mkdir(exist_ok=True)
if not DB.exists():
    raise FileNotFoundError(f'Missing database: {DB}')
with sqlite3.connect(DB) as con:
    df = pd.read_sql_query('SELECT * FROM launches', con)
if df.empty:
    raise ValueError('No launches in database')
for c in ['Latitude', 'Longitude', 'PayloadMass', 'Class']:
    df[c] = pd.to_numeric(df[c], errors='coerce')

sites = df.dropna(subset=['Latitude','Longitude']).groupby('LaunchSite', as_index=False).agg(
    latitude=('Latitude','mean'), longitude=('Longitude','mean'), launches=('Class','size'), success_rate=('Class','mean'))
map_ = folium.Map(location=[29,-95], zoom_start=4, tiles=None)
for _, s in sites.iterrows():
    label = f"<b>{s['LaunchSite']}</b><br>Launches: {int(s['launches'])}<br>Landing success: {s['success_rate']:.1%}"
    folium.CircleMarker([s['latitude'],s['longitude']], radius=10, color='#1765a3', fill=True, fill_opacity=.8,
                        tooltip=s['LaunchSite'], popup=folium.Popup(label, max_width=250)).add_to(map_)
map_.save(str(OUT / 'launch_sites_map.html'))

site_fig = px.bar(sites, x='LaunchSite', y='success_rate', title='Landing success by launch site',
                  hover_data=['launches'], labels={'success_rate':'Landing success rate'})
site_fig.update_yaxes(tickformat='.0%')
site_fig.write_html(str(OUT/'site_success_interactive.html'))

app = Dash(__name__)
site_options = [{'label':'All Sites','value':'ALL'}] + [{'label':s,'value':s} for s in sorted(df['LaunchSite'].dropna().unique())]
min_payload = float(df['PayloadMass'].min())
max_payload = float(df['PayloadMass'].max())
app.layout = html.Div(style={'fontFamily':'Arial','maxWidth':'1100px','margin':'auto','padding':'25px'}, children=[
    html.H1('SpaceX Falcon 9 Landing Analysis'),
    html.P('Interactive dashboard from the local IBM Capstone launch dataset. Class 1 = successful landing.'),
    html.Label('Launch site'),
    dcc.Dropdown(id='site', options=site_options, value='ALL', clearable=False),
    html.Label('Payload mass (kg)', style={'display':'block','marginTop':'20px'}),
    dcc.RangeSlider(id='payload', min=min_payload, max=max_payload, step=100,
                    value=[min_payload,max_payload], tooltip={'placement':'bottom','always_visible':True}),
    html.Div(id='metrics', style={'marginTop':'25px','fontWeight':'bold'}),
    dcc.Graph(id='scatter'), dcc.Graph(id='orbit')
])
@app.callback(Output('scatter','figure'),Output('orbit','figure'),Output('metrics','children'),
              Input('site','value'),Input('payload','value'))
def update(site, payload):
    d = df[(df['PayloadMass'] >= payload[0]) & (df['PayloadMass'] <= payload[1])].copy()
    if site != 'ALL': d = d[d['LaunchSite'] == site]
    scatter = px.scatter(d, x='FlightNumber', y='PayloadMass', color=d['Class'].map({0:'Failure',1:'Success'}),
                         hover_data=['LaunchSite','Orbit'], title='Flight number vs payload mass', labels={'color':'Landing'})
    if len(d):
        orbit = d.groupby('Orbit',as_index=False).agg(success_rate=('Class','mean'),launches=('Class','size'))
        bar = px.bar(orbit, x='Orbit', y='success_rate', hover_data=['launches'], title='Landing success by orbit')
        bar.update_yaxes(tickformat='.0%', range=[0,1])
        metrics = f"Filtered launches: {len(d)} | Successful landings: {int(d['Class'].sum())} | Success rate: {d['Class'].mean():.1%}"
    else:
        bar = px.bar(title='No launches match these filters')
        metrics = 'No launches match these filters.'
    return scatter,bar,metrics

if __name__ == '__main__':
    print(f'Map saved: {OUT / "launch_sites_map.html"}')
    print(f'Interactive chart saved: {OUT / "site_success_interactive.html"}')
    print('Dash dashboard starting at http://127.0.0.1:8050')
    app.run(debug=False, host='127.0.0.1', port=8050)
