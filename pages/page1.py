import dash
from dash import html, dash_table, dcc
import plotly.express as px

def create_layout(data) -> html.Div:
    df_athelete = data['df_athlete']
    df_athelete['Medal'].fillna('No Medal', inplace=True)

    medal_count = df_athelete.groupby(['NOC', 'Medal']).Medal.count().reset_index(name='Medals')
    medal_count = medal_count[medal_count['Medal'] != 'No Medal']
    
    color_discrete_map = {
    'Gold': 'gold',
    'Silver': 'silver',
    'Bronze': 'brown',
    }

    figure = px.bar(medal_count, x="NOC", y="Medals", color="Medal", barmode="stack", color_discrete_map=color_discrete_map)

    gender_count = df_athelete.groupby(['Sex', 'Year']).Sex.count().reset_index(name='Athletes')

    color_discrete_map = {
    'M': 'blue',
    'F': 'pink',
    }

    combined_gender_count = gender_count.pivot(index='Year', columns='Sex', values='Athletes').reset_index()

    stacked_bar_figure = px.bar(gender_count, x="Year", y="Athletes", color="Sex", barmode="stack", color_discrete_map=color_discrete_map)
    line_figure = px.line(combined_gender_count, x="Year", y=["M", "F"], color_discrete_map=color_discrete_map)

    return html.Div([
        html.H2(children='Medals'),
        dcc.Graph(figure=figure),
        html.H2(children='Number of men and women over time'),
        dcc.Graph(figure=stacked_bar_figure),
        dcc.Graph(figure=line_figure),
    ])
