# Import packages
import dash
from dash import Dash, html, dcc, Input, Output, ALL

# Initialize the app
app = Dash(__name__, use_pages=True)

# -------------------- Sidebar --------------------
sidebar = html.Div(
    [
        html.Div([
            html.Div([
                html.H2('Projet Dash', className='sidebar-title'),
                html.P(
					[
                        "TREMBLEAU Thibault",
                        html.Br(),
                        "BRUSTOLIN Lucas",
                        html.Br(),
                        "BOYER Alexis"
                    ],
                    className='sidebar-subtitle'
                )
            ], className='sidebar-header'),
            html.Ul([
				html.Li(
					dcc.Link(page['name'], href=page['relative_path'], className='sidebar-item-link'),
                    id={'type': 'sidebar-item', 'index': page['relative_path']},
                    className='sidebar-item'
                ) for page in dash.page_registry.values()
            ], className='sidebar-menu')
        ], className='sidebar-container')
    ],
    className='sidebar'
)

@app.callback(
    Output({'type': 'sidebar-item', 'index': ALL}, 'className'),
    [Input('url', 'pathname'), Input({'type': 'sidebar-item', 'index': ALL}, 'children')]
)
def set_active_link(pathname, items):
    return [
        'sidebar-item active' if pathname == item['props']['href'] else 'sidebar-item'
        for item in items
    ]

# -------------------- App layout --------------------
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(
        dcc.Loading(id='loading', type='default', children=
            html.Div(dash.page_container, className='page-container')
        ),
        id='page-content',
        className='page-content'
    ),
	sidebar
])

if __name__ == '__main__':
    app.run(debug=True)
