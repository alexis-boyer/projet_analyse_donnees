import dash
from dash import html, dash_table, dcc
import plotly.express as px

def create_layout(data) -> html.Div:
    df_athelete = data['df_athlete']

    # Replace NA by No Medal
    df_athelete['Medal'].fillna('No Medal', inplace=True)

    # Medals by country
    medal_count_by_country = df_athelete.groupby(['NOC', 'Medal']).Medal.count().reset_index(name='Medals count')
    medal_count_by_country = medal_count_by_country[medal_count_by_country['Medal'] != 'No Medal']

    # Medals by gender and country
    medal_count_by_gender_and_country = df_athelete.groupby(['NOC', 'Medal', 'Sex']).Medal.count().reset_index(name='Medals count')

    # Medals for women by country
    women_medal_count = medal_count_by_gender_and_country[medal_count_by_gender_and_country['Sex'] == 'F']
    women_medal_count = women_medal_count[women_medal_count['Medal'] != 'No Medal']

    #Medals for men by country
    men_medal_count = medal_count_by_gender_and_country[medal_count_by_gender_and_country['Sex'] == 'M']
    men_medal_count = men_medal_count[men_medal_count['Medal'] != 'No Medal']

    df_height = df_athelete.dropna(subset=['Height'])
    df_weight = df_athelete.dropna(subset=['Weight'])
    
    medal_color_mapping = {
    'Gold': 'gold',
    'Silver': 'silver',
    'Bronze': 'brown',
    }

    gender_count = df_athelete.groupby(['Sex', 'Year']).Sex.count().reset_index(name='Athletes')

    gender_color_mapping = {
    'M': 'blue',
    'F': 'red',
    }

    combined_gender_count = gender_count.pivot(index='Year', columns='Sex', values='Athletes').reset_index()

    return html.Div([
        html.H2(children='Medals by nations'),
        dcc.Graph(figure=px.bar(medal_count_by_country, x="NOC", y="Medals count", color="Medal", barmode="stack", color_discrete_map=medal_color_mapping)),
        html.H2(children='Medals for men by nations'),
        dcc.Graph(figure=px.bar(men_medal_count, x="NOC", y="Medals count", color="Medal", labels={'Medals': 'Count', 'NOC': 'Country', 'Medal': 'Medal Type'}, color_discrete_map=medal_color_mapping)),
        html.H2(children='Medals for women by nations'),
        dcc.Graph(figure=px.bar(women_medal_count, x="NOC", y="Medals count", color="Medal", labels={'Medals': 'Count', 'NOC': 'Country', 'Medal': 'Medal Type'}, color_discrete_map=medal_color_mapping)),
        html.H2(children='Number of men and women over time'),
        dcc.Graph(figure=px.bar(gender_count, x="Year", y="Athletes", color="Sex", barmode="stack", color_discrete_map=gender_color_mapping)),
        dcc.Graph(figure=px.line(combined_gender_count, x="Year", y=["M", "F"], color_discrete_map=gender_color_mapping)),
        html.H2(children='Evolution of Athletes\' Height Over Time'),
        dcc.Graph(figure=px.box(df_height, x='Year', y='Height', color='Sex', color_discrete_map=gender_color_mapping)),
        html.H2(children='Evolution of Athletes\' Weight Over Time'),
        dcc.Graph(figure=px.box(df_weight, x='Year', y='Weight', color='Sex', color_discrete_map=gender_color_mapping)),
    ])
