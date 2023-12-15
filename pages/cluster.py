import dash
from dash import html, dash_table, dcc
import plotly.express as px

def create_layout(data) -> html.Div:
    return html.Div([
        html.H2(children='Page 2'),
        dash_table.DataTable(data=data['df_athlete'].to_dict('records'), page_size=50),
        dcc.Graph(figure=px.histogram(data['df_athlete'], x='Year', y='Age', histfunc='avg')),
        # dash_table.DataTable(data['df_athlete'].groupby('NOC')['NOC'].transform('count'))
    ])
