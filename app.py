# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Initialize the app
app = Dash(__name__)

# Incorporate data
df = pd.read_csv('./data/athlete_events.csv')

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=50),
    dcc.Graph(figure=px.histogram(df, x='Year', y='Age', histfunc='avg')),
    dash_table.DataTable(df.groupby('NOC')['NOC'].transform('count'))
])

if __name__ == '__main__':
    app.run(debug=True)
