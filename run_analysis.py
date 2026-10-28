from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv'
local = ROOT / 'dataset_part_2.csv'
if local.exists():
    df = pd.read_csv(local)
else:
    print('Downloading IBM training dataset...')
    df = pd.read_csv(URL)
    df.to_csv(local,index=False)
required = {'Class','LaunchSite','Orbit','PayloadMass','FlightNumber'}
assert required.issubset(df.columns), f'Missing columns: {required-set(df.columns)}'
df['Class'] = pd.to_numeric(df['Class'],errors='coerce')
df = df.dropna(subset=['Class']).copy()
df['Class'] = df['Class'].astype(int)
with open(OUT/'summary.txt','w',encoding='utf-8') as f:
    f.write(f'Dataset rows: {len(df)}\nLanding success rate: {df.Class.mean():.2%}\n')
    f.write('Launch sites:\n'+df.groupby('LaunchSite')['Class'].agg(['count','mean']).to_string()+'\n')
    f.write('Orbit success:\n'+df.groupby('Orbit')['Class'].agg(['count','mean']).to_string()+'\n')
    f.write('Missing values:\n'+df.isna().sum().to_string()+'\n')
for col,filename in [('LaunchSite','site_success.png'),('Orbit','orbit_success.png')]:
    fig,ax=plt.subplots(figsize=(10,5))
    df.groupby(col)['Class'].mean().sort_values().mul(100).plot.bar(ax=ax)
    ax.set_ylabel('Successful landing (%)');ax.set_title(f'Landing success by {col}')
    ax.set_ylim(0,105);fig.tight_layout();fig.savefig(OUT/filename,dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,5))
for label,g in df.groupby('Class'):
    ax.scatter(g['FlightNumber'],g['PayloadMass'],label=f'Class {label}',alpha=.75)
ax.set_xlabel('Flight number');ax.set_ylabel('Payload mass (kg)');ax.legend();fig.tight_layout()
fig.savefig(OUT/'flight_payload.png',dpi=180);plt.close(fig)
conn=sqlite3.connect(OUT/'spacex.db')
df.to_sql('launches',conn,if_exists='replace',index=False)
queries={'site_summary':'SELECT LaunchSite, COUNT(*) AS launches, ROUND(AVG(Class)*100,1) AS success_pct FROM launches GROUP BY LaunchSite ORDER BY success_pct DESC', 'orbit_summary':'SELECT Orbit, COUNT(*) AS launches, ROUND(AVG(Class)*100,1) AS success_pct FROM launches GROUP BY Orbit ORDER BY launches DESC','overall':'SELECT COUNT(*) AS launches, SUM(Class) AS successful_landings, ROUND(AVG(Class)*100,1) AS success_pct FROM launches'}
with open(OUT/'sql_results.txt','w') as f:
    for title,q in queries.items():
        f.write(f'\n-- {title}\n{q}\n'+pd.read_sql_query(q,conn).to_string(index=False)+'\n')
conn.close()
features=[c for c in ['PayloadMass','Flights','GridFins','Reused','Legs','Block','ReusedCount','Orbit','LaunchSite'] if c in df]
X=df[features].copy();y=df['Class']
for c in X.select_dtypes(include='bool').columns:X[c]=X[c].astype(int)
num=X.select_dtypes(include='number').columns.tolist();cat=[c for c in X if c not in num]
pre=ColumnTransformer([('num',Pipeline([('imputer',SimpleImputer(strategy='median')),('scale',StandardScaler())]),num),('cat',Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore'))]),cat)])
model=Pipeline([('prep',pre),('model',LogisticRegression(max_iter=2000))])
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
model.fit(Xtrain,ytrain);pred=model.predict(Xtest)
with open(OUT/'ml_results.txt','w') as f:
    f.write(f'Train rows: {len(Xtrain)} | Test rows: {len(Xtest)}\nTest accuracy: {accuracy_score(ytest,pred):.4f}\n')
    f.write(classification_report(ytest,pred,zero_division=0))
ConfusionMatrixDisplay.from_predictions(ytest,pred);plt.tight_layout();plt.savefig(OUT/'confusion_matrix.png',dpi=180);plt.close()
print('Analysis complete. Review files in:',OUT)
