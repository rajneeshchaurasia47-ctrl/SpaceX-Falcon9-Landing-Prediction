"""Folium interactive map: 3 launch sites, 90 outcome markers, MarkerCluster and proximity lines.
Place IBM dataset_part_2.csv at repository root. The four landmark coordinates are
historic course-example reference points, NOT independently verified closest features.
"""
from pathlib import Path
import math
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
root = Path(__file__).resolve().parents[1]
df = pd.read_csv(root / "dataset_part_2.csv")
m = folium.Map(location=[29.7, -92], zoom_start=4, tiles="CartoDB positron", control_scale=True)
for site, group in df.groupby("LaunchSite"):
    latitude = float(group.Latitude.iloc[0])
    longitude = float(group.Longitude.iloc[0])
    count = len(group)
    successes = int(group.Class.sum())
    folium.Circle([latitude, longitude], radius=16000, color="#096e90",
                  fill=True, fill_opacity=0.08).add_to(m)
    folium.Marker([latitude, longitude],
                  popup=f"{site}: {successes}/{count} successful landings",
                  icon=folium.Icon(color="blue", icon="flag")).add_to(m)
cluster = MarkerCluster(name="Landing outcomes").add_to(m)
for _, r in df.iterrows():
    color = "green" if int(r.Class) == 1 else "red"
    folium.Marker([float(r.Latitude), float(r.Longitude)],
                  popup=f"Flight {int(r.FlightNumber)} | {r.LaunchSite} | landing Class {int(r.Class)}",
                  icon=folium.Icon(color=color, icon="info-sign")).add_to(cluster)
def haversine(a,b,c,d):
    radius=6371.0
    p1,p2=math.radians(a),math.radians(c)
    delta_lat=p2-p1
    delta_lon=math.radians(d-b)
    t=math.sin(delta_lat/2)**2+math.cos(p1)*math.cos(p2)*math.sin(delta_lon/2)**2
    return 2*radius*math.atan2(math.sqrt(t),math.sqrt(1-t))
origin=df.loc[df.LaunchSite=="CCAFS SLC 40"].iloc[0]
a,b=float(origin.Latitude),float(origin.Longitude)
# Coordinates reproduced from a published historical IBM Folium lab walkthrough.
places={
  "Coastline reference":(28.56409,-80.56806),
  "Railway reference":(28.57217,-80.58528),
  "Highway reference":(28.56385,-80.57088),
  "City reference":(28.10469,-80.64784)
}
for name,(lat,lon) in places.items():
    km=haversine(a,b,lat,lon)
    folium.Marker([lat,lon],tooltip=f"{name}: {km:.2f} km",
                  icon=folium.Icon(color="orange", icon="pushpin")).add_to(m)
    folium.PolyLine([[a,b],[lat,lon]],color="#e09b28",weight=3,
                    tooltip=f"{km:.2f} km straight-line").add_to(m)
folium.LayerControl().add_to(m)
MousePosition().add_to(m)
out=root / "interactive" / "launch_sites_proximity_complete.html"
m.save(str(out))
print("Saved:", out, "launch markers:", len(df), "landmark distances:",
      {k:round(haversine(a,b,*p),3) for k,p in places.items()})
