import dash_bootstrap_components as dbc
from flask import *
import pandas as pd
import os
from datetime import datetime,timedelta
import plotly.express as px
from dash import Dash,dcc,html, Input, Output

app = Flask(__name__)
dash_app = Dash(__name__, server = app, url_base_pathname='/oprjdash/',external_stylesheets=[dbc.themes.ZEPHYR])

path = "Z:\PSG\FYear Project\Project\Flask Web App\Website\Dataset\Log Sheets"
files = []
mhrs = []
a=[]
file = 0
id_ = ['8180','VK-2510',
'SV1312', 'KR-0010'
'537016','537017','537056'
]
# proj = ['2490HD (06) ']
proj = ['9020 (01) ']
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
        # fileloc = path+"/"+files[0]
print(files)

id_name=[]
for i in files:
    i_ = i.replace('.csv','').replace("_"," ")
    id_name.append(i_)
print(id_name)

tdf = []
for i in files:
    df = pd.read_csv(path+"/"+i, usecols=['DATE','PROJECT','PROGRESS','MAN_HOURS'], skip_blank_lines=True)
    print(df)
    for j in range(len(df)):
        # print(j)
        date=(datetime.strptime(df.loc[j,"DATE"],"%m/%d/%Y")).strftime("%m/%d/%Y")
        if date in dates:
            a.append((df.loc[j]).tolist())
    dff = pd.DataFrame(a, columns=['DATE','PROJECT','MAN_HOURS','PROGRESS'])
    dff = dff[dff['PROJECT'].isin(proj)]
    tdf.append(dff)
# print(a)
for i in tdf:
    mhrs.append(i['MAN_HOURS'].sum())
print(tdf)
print(mhrs)

# drop = dcc.Dropdown(id='progress_bar', options=[{'label':'Yet to Start','value':'Yet to Start'},
#                                                 {'label':'0% - 25%','value':'0% - 25%'},
#                                                 {'label':'25% - 50%','value':'25% - 50%'},
#                                                 {'label':'50% - 75%','value':'50% - 75%'},
#                                                 {'label':'75% - 100%','value':'75% - 100%'},
#                                                 {'label':'Completed','value':'Completed'}],value='0% - 25%')

pie_chart = px.pie(names=id_name ,values = mhrs, title = proj[0],)
pie_chart.update_traces(textposition = 'outside', rotation = 150, textinfo = 'percent+value+label')
pie_chart.update_layout(showlegend = False)



dr_card = dbc.Card([
            dbc.CardBody([
                html.H1(d1.strftime('%d/%m/%Y')+' - '+ d2.strftime('%d/%m/%Y') ,style={'text-align':'center','font-size':'28pt'}),
                html.H3('Selected Date Range', style={'text-align':'center', 'color':'#003f72'})
            ])
        ],color='light',style={'height':'150px'})
mhr_card = dbc.Card([
            dbc.CardBody([
                html.H1(sum(mhrs),style={'text-align':'center','font-size':'28pt'}),
                html.H3("Total Man Hours",style={'text-align':'center', 'color':'#003f72'})
            ])
            ],color='light',style={'height':'150px'})
employeelist_card = dbc.Card([
    dbc.CardBody([
        html.H1('Employees Worked:',style={'text-align':'center','font-size':'22pt', 'color':'#003f72'}),
        html.Br(),
        *[html.H3(text, style={"font-size":"15pt"}) for text in id_name]
],style={'overflowY': 'scroll'})
],color='light',style={'height':'450px'})
prjname_card = dbc.Card([
    dbc.CardBody([
        html.H1('ID: '+'1510',style={'text-align':'center','font-size':'28pt',}),
        html.H3(proj[0],style={'text-align':'center'}),
    ])
],color='light',style={'height':'150px'})
prjsdate_card = dbc.Card([
    dbc.CardBody([
        html.H1('03/01/2022',style={'text-align':'center','font-size':'28pt'}),
        html.H3('Project Start Date',style={'text-align':'center', 'color':'#003f72'}),
    ])
],color='light',style={'height':'150px'})
prjedate_card = dbc.Card([
    dbc.CardBody([
        html.H1('31/12/2024',style={'text-align':'center','font-size':'28pt'}),
        html.H3('Targeted End Date',style={'text-align':'center', 'color':'#003f72'}),
    ])
],color='light',style={'height':'150px'})
cprjdate_card = dbc.Card([
    dbc.CardBody([
        html.H1('-',style={'text-align':'center','font-size':'28pt'}),
        html.H3('Completion Date',style={'text-align':'center', 'color':'#003f72'}),
    ])
],color='light',style={'height':'150px'})

rows = [dbc.Row([
    dbc.Col(dr_card,width=6),
    dbc.Col(mhr_card,width=6),
]),
dbc.Row([
    dbc.Col(prjname_card,width=3),
    dbc.Col(prjsdate_card,width=3),
    dbc.Col(prjedate_card,width=3),
    dbc.Col(cprjdate_card,width=3)
]),
dbc.Row([dbc.Col([
    dbc.Card([
        dcc.Graph(id='oneproject_pie',figure=pie_chart),
    ],color = 'light')
    ],width = 8),
    dbc.Col(employeelist_card,width=4),
])]

dash_app.layout = html.Div(dbc.Container(rows))

@app.route('/oprjdash/')
def dashboard():
    return render_template('dashboard.html',dash_app=dash_app)

if __name__ == '__main__':
    app.run(debug = True,port=8180)




