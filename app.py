# Import packages
import dash
from dash import Dash, html, dcc, Input, Output, ALL
from pages import cluster, home, overview, network
import pandas as pd

# Initialize the app
app = Dash(
    __name__,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
    title='Projet Dash'
)

# Initialize data
df_athlete = pd.read_csv('./data/athlete_events.csv')
df_noc = pd.read_csv('./data/noc_regions.csv')

# Enumerate pages
pages = [
    {
        'id': 'home',
        'name': 'Page d\'accueil',
        'layout': home.create_layout()
    },
    {
        'id': 'page1',
        'name': 'Overview',
        'layout': overview.create_layout({'df_athlete': df_athlete, 'df_noc': df_noc})
    },
    {
        'id': 'cluster',
        'name': 'Cluster',
        'layout': cluster.create_layout({'df_athlete': df_athlete, 'df_noc': df_noc})
    },
    {
        'id': 'network',
        'name': 'Network',
        'layout': network.create_layout({'df_athlete': df_athlete, 'df_noc': df_noc})
    }
]

# -------------------- Sidebar --------------------
sidebar = html.Div(className='sidebar', children=[
    html.Div(className='sidebar-container', children=[
        html.Div(className='sidebar-header', children=[
            html.H2('Projet Dash', className='sidebar-title'),
            html.P(className='sidebar-subtitle', children=[
                "TREMBLEAU Thibault",
                html.Br(),
                "BRUSTOLIN Lucas",
                html.Br(),
                "BOYER Alexis"
            ])
        ]),
        dcc.Tabs(id='sidebar-menu', value=pages[0]['id'], className='sidebar-menu', children=[
            dcc.Tab(
                label=page['name'],
                value=page['id'],
                className='sidebar-item',
                selected_className='active'
            ) for page in pages
        ])
    ])
])

# -------------------- App layout --------------------
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='page-container', className='page-container', children=
        dcc.Loading(id='loading', className='page-loading', type='default', children=
            html.Div(id='page-content', className='page-content')
        )
    ),
    sidebar
])

# -------------------- Render pages --------------------
# Store?: https://github.com/salesforce/Merlion/blob/01c3fc3406ebf19798cedcddbe829ae5339e1424/merlion/dashboard/server.py
@app.callback(
    Output('page-content', 'children'),
    [Input('sidebar-menu', 'value')]
)
def render_content(tab):
    if tab is None:
        return home.create_layout()
    else:
        for page in pages:
            if tab == page['id']:
                return page['layout']

if __name__ == '__main__':
    app.run(debug=True)
