import dash
from dash import html

dash.register_page(__name__, path='/', name='Page d\'accueil')

layout = html.Div([
    html.H1('Ceci est la page d\'accueil')
])
