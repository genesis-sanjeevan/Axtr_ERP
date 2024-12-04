import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('Dataset\Log Sheets\8180-S_MOHAMED_RAUF_ALI_S.csv')

app = dash.Dash(__name__,external_stylesheets=[dcc.themes.SOLAR])