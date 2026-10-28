"""Plotly Dash: dropdown + payload slider, all-site / selected-site pie and outcome scatter.
Install: pip install dash plotly pandas ; run python interactive/dash_pie_scatter_complete.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
data=pd.read_csv(Path(__file__).resolve().parents[1]/"dataset_part_2.csv")
app=Dash(__name__)
choices=[{"label":"All sites","value":"ALL"}]+[
    {"label":v,"value":v} for v in sorted(data.LaunchSite.unique())]
app.layout=html.Div(style={"fontFamily":"Arial","maxWidth":"1000px","margin":"auto"},children=[
  html.H1("SpaceX Falcon 9 landing outcomes"),
  dcc.Dropdown(id="site-dropdown",options=choices,value="ALL",clearable=False),
  html.P("Filter payload mass (kg):"),
  dcc.RangeSlider(id="payload-slider",min=0,max=16000,step=1000,value=[0,16000],
                  marks={v:f"{v//1000}t" for v in range(0,16001,2000)}),
  dcc.Graph(id="pie"),dcc.Graph(id="scatter"),
  html.P("Historical course data; Class 1 = recovered booster.")
])
@app.callback(Output("pie","figure"),Output("scatter","figure"),
              Input("site-dropdown","value"),Input("payload-slider","value"))
def update(site,rng):
  df=data[(data.PayloadMass>=rng[0])&(data.PayloadMass<=rng[1])].copy()
  if site!="ALL":df=df[df.LaunchSite==site]
  df["Landing"]=df.Class.map({1:"Success",0:"Failure"})
  if site=="ALL":
    counts=df[df.Class==1].groupby("LaunchSite").size().reset_index(name="Successful landings")
    pie=px.pie(counts,names="LaunchSite",values="Successful landings",
               title="All sites: successful landing share")
  else:
    counts=df.groupby("Landing").size().reset_index(name="Launches")
    pie=px.pie(counts,names="Landing",values="Launches",
               title=f"{site}: successful versus unsuccessful recovery")
  scatter=px.scatter(df,x="PayloadMass",y="Class",color="Landing",
          hover_data=["FlightNumber","LaunchSite","Orbit"],
          title="Payload mass versus landing outcome")
  scatter.update_yaxes(tickvals=[0,1],ticktext=["Failure","Success"])
  return pie,scatter
if __name__=="__main__":app.run(debug=False)
