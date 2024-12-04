import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime,timedelta
import numpy as np
from flask import Flask, render_template

app = Flask(__name__)
dash_app = Dash(__name__, server= app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.ZEPHYR])

filename = ['SV-0123_SIVARAMAN_S','RF-2907_MOHAMED_RAUF_ALI_S']

ls = pd.read_csv("Z:\Python Files\Plotly & Dash\Plotly\Data\Actual Data\RF-2907_MOHAMED_RAUF_ALI_S.csv")
# ls = pd.read_csv("Z:\Python Files\Plotly & Dash\Plotly\Data\Actual Data\SV-0123_SIVARAMAN_S.csv")

x = '04/01/2022'
y = '04/20/2022'

d1=datetime.strptime(x,"%m/%d/%Y")
d2=datetime.strptime(y,"%m/%d/%Y")
delta=d2-d1

dates=[]
for i in range(delta.days+1):
    day=(d1+timedelta(days=i)).strftime("%m/%d/%Y")
    dates.append(day)

a=[]
for i in range(len(ls)):
    date=(datetime.strptime(ls.loc[i,"DATE"],"%m/%d/%Y")).strftime("%m/%d/%Y")
    if date in dates:
        a.append((ls.loc[i]).tolist())
# print(a)
if a == []:
    rows = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("No logs Entered", style={'text-align': 'center', 'font-size' : '20px', 'font-color': 'blue','margin-top':'25%'})
        ], width=12),        
    ]),
    dbc.Row([
        dbc.Col([
            html.H1("No logs entered between {x}-{y}".format(x=x,y=y), style={'text-align': 'center', 'font-size' : '16px', 'font-color': 'blue'})
        ], width=12)
        ])
    ])
    

else:
    df=pd.DataFrame(a,columns=['DATE','PROJECT','FIELD_OF_WORK','SECTION','DAILY_ACTIVITY','MAN_HOURS'])
    dfs = df['MAN_HOURS'].sum()
    print(df)

    proj_pie = px.pie(data_frame=df, names='PROJECT', values='MAN_HOURS', title='PROJECTS WORKED', hover_data= ['PROJECT'])
    proj_pie.update_traces(textposition = 'outside', rotation = 180, textinfo= 'label+percent')
    proj_pie.update_layout(showlegend = False, plot_bgcolor='rgb(217, 222, 221)')

    fldow_pie = px.pie(data_frame=df, names='FIELD_OF_WORK', values='MAN_HOURS', title='FIELD OF WORK CONCENTRTED', labels='FIELD_OF_WORK', template='plotly_white')
    fldow_pie.update_traces(textposition = 'outside', rotation = 180,textinfo= 'label+percent')
    fldow_pie.update_layout(showlegend = False)

    sec_pie = px.pie(data_frame=df, names='SECTION', values='MAN_HOURS', title='SECTIONS WORKED', template='plotly_white')
    sec_pie.update_traces(textposition = 'outside', rotation = 180, textinfo= 'label+percent')
    sec_pie.update_layout(showlegend = False)

    daila_pie = px.pie(data_frame=df, names='DAILY_ACTIVITY', values='MAN_HOURS', title='DAILY ACTIVITY WORKED', template='plotly_white')
    daila_pie.update_traces(textposition = 'outside', rotation = 180, textinfo= 'label+percent')
    daila_pie.update_layout(showlegend = False)

    proj_bar = px.bar(data_frame=df, x='PROJECT', y='MAN_HOURS', title='Project', color='PROJECT')
    proj_bar.update_traces()
    proj_bar.update_layout(showlegend = False)

    name_card = dbc.Card([
        dbc.CardBody([
            html.H1('S SIVARAMAN', style={'text-align':'center', 'color':'#003f72'})
        ])
    ],color='light')
    id_card = dbc.Card([
        dbc.CardBody([
            html.H1('1312', style={'text-align':'center', 'color':'#003f72'})
        ])
    ],color='light')

    dr_card = dbc.Card([
        dbc.CardBody([
            html.H1(d1.strftime('%d/%m/%Y')+' - '+ d2.strftime('%d/%m/%Y') ,style={'text-align':'center',
            'font-size':'28pt'
            }),
            html.H3('Selected Date Range', style={'text-align':'center', 'color':'#003f72'})])
        ], color='light', style={'height':'125px','width':'auto'})
    mhcrd = dbc.Card([
        dbc.CardBody([
            html.H1(dfs,style={'text-align':'center','font-weight':'bold'}),
            html.H3('Man Hour(s)',style={'text-align':'center', 'color':'#003f72'})])
        ], color='light', style={'height':'125px','width':'auto'})
    efficiency = dbc.Card([
        dbc.CardBody([
            html.H1("96%", style={'text-align':'center', 'font-weight':'bold'}),
            html.H3("Efficiency", style={'text-align':'center', 'color':'#003f72'})
        ])
    ], color='light', style={'height':'125px','width':'auto'})

    rows = [dbc.Row([
        dbc.Col(name_card, width=6),
        dbc.Col(id_card, width=6)
    ]),
    dbc.Row([
        dbc.Col(dr_card, width=6),
        dbc.Col(mhcrd, width=3),
        dbc.Col(efficiency, width=3),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            dcc.Graph(id='project_pie', figure=proj_pie)
            ], color='light')
        ], width=12),]),
   dbc.Row([dbc.Col([
            dbc.Card([
            dcc.Graph(id='field_o_work', figure=fldow_pie)
            ], color='light')
        ], width=12),]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            dcc.Graph(id='sec_pie', figure=sec_pie)
            ], color='light')
        ], width=12)]),
    dbc.Row([dbc.Col([
            dbc.Card([
            dcc.Graph(id='daila_pie', figure=daila_pie)
            ], color='light')
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
            dcc.Graph(id='project_bar', figure=proj_bar)
            ], color='light')
        ], width=12)
    ])]

dash_app.layout = html.Div(dbc.Container(rows))

@app.route('/')
def index():
    return "Hello world!"

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html', dash_app=dash_app)

if __name__=="__main__":
    app.run(debug=True, port=8080)