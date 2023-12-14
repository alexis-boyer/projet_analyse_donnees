import dash
from dash import html

def create_layout() -> html.Div:
    return html.Div([
        html.H2('Ceci est la page d\'accueil')
    ])
