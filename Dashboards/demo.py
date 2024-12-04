from dash import Dash,html,dcc 
import dash_bootstrap_components as dbc
from flask import *
import pandas as pd
import os
from datetime import datetime,timedelta
import plotly.express as px

app = Flask(__name__)
dash_app = Dash(__name__, server = app, url_base_pathname='/mprjdash/',external_stylesheets=[dbc.themes.ZEPHYR])

path = "Z:\PSG\FYear Project\Project\Flask Web App\Website\Dataset\Log Sheets"
files = []
mhrs = []
a=[]
file = 0
id_ = ['8180','SV1312','VK-2510']
proj = ['2490HD (06) ','9020 (01) ',
# '300i (07) '
]
x = '12/01/2022'
y = '01/30/2023'

d1=datetime.strptime(x,"%m/%d/%Y")
d2=datetime.strptime(y,"%m/%d/%Y")
delta=d2-d1

dates=[]
for i in range(delta.days+1):
    day=(d1+timedelta(days=i)).strftime("%m/%d/%Y")
    dates.append(day)

for i in os.listdir(path):
    for j in id_:
        if os.path.isfile(os.path.join(path,i)) and j in i:
            files.append(i)
            file = file+1
        if file == 0:
            print("No Log Sheet Of User Found")
        fileloc = path+"/"+files[0]
print(files)

id_name=[]
for i in files:
    i_ = i.replace('.csv','').replace("_"," ")
    id_name.append(i_)
print(id_name)

tdf = []
for i in files:
    df = pd.read_csv(path+"/"+i, usecols=['DATE','PROJECT','PROGRESS','MAN_HOURS'], skip_blank_lines=True)
    # print(df)
    for j in range(len(df)):
        date=(datetime.strptime(df.loc[j,"DATE"],"%m/%d/%Y")).strftime("%m/%d/%Y")
        if date in dates:
            a.append((df.loc[j]).tolist())
    dff = pd.DataFrame(a,columns=['DATE','PROJECT','MAN_HOURS','PROGRESS'])
    # print(dff)
    # dff = dff[dff['PROJECT'].str.contains('2490')]
    dff = dff.loc[dff['PROJECT'].isin(proj)]
    # print(dff)
    tdf.append(dff)
# print(a)
for i in tdf:
    mhrs.append(i['MAN_HOURS'].sum())
print(tdf)
print(mhrs)

for i in tdf:
    i = i[i.loc[]]
    # pie_chart = px.pie(data_frame=i, names=id_name ,values = i[i.loc['PROJECT'].str.contains('2490')], title = proj[0],)
    # pie_chart.update_traces(textposition = 'outside', rotation = 150, textinfo = 'percent+label+value')
    # pie_chart.show()


# @app.route('/mprjdash/')
# def dashboard():
#     return render_template('dashboard.html',dash_app=dash_app)

# if __name__ == '__main__':
#     app.run(debug = True,port=8180)