import dash
from dash import html, dash_table, dcc
import plotly.express as px

def create_layout(data) -> html.Div:
    df_athelete = data['df_athlete']
    df_athelete['Medal'].fillna('No Medal', inplace=True)

    medal_count = df_athelete.groupby(['NOC', 'Medal']).Medal.count().reset_index(name='counts')
    medal_count = medal_count[medal_count['Medal'] != 'No Medal']
    
    figure = px.bar(medal_count, x="NOC", y="counts", color="Medal", barmode="group")

    return html.Div([
        html.H2(children='Page 1'),
        #dash_table.DataTable(df_athelete.to_dict('records'), [{"name": i, "id": i} for i in df_athelete.loc[:,["Name", "Age", "Weight"]]], page_size=50),
        dcc.Graph(id='medal-distribution-chart', figure=figure),
        # dash_table.DataTable(data['df_athlete'].groupby('NOC')['NOC'].transform('count'))
    ])
