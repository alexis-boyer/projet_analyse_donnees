import dash
from dash import html, dash_table, dcc
import plotly.express as px
from main_data import df

dash.register_page(__name__)

layout = html.Div([
    html.Div(children='Page 1'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=50),
    dcc.Graph(figure=px.histogram(df, x='Year', y='Age', histfunc='avg')),
    # dash_table.DataTable(df.groupby('NOC')['NOC'].transform('count'))
])
