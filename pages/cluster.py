import dash
from dash import html, dash_table, dcc
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
import plotly.graph_objects as go
import plotly.express as px


def create_layout(data) -> html.Div:
    figGMM = create_cluster_height_weight(data['df_athlete'])
    figSex = create_athlete_sex_fig(data['df_athlete'])
    return html.Div([
        html.H2(children='Cluster'),
        html.H3(children='Homme/Femme'),
        dcc.Graph(figure = figGMM),
        dcc.Graph(figure = figSex)
        # dash_table.DataTable(data['df_athlete'].groupby('NOC')['NOC'].transform('count'))
    ])

def create_cluster_height_weight(athletes_df):
    
    # standarization of numerical data
    athletes_df.dropna(subset=['Height', 'Weight'], inplace=True)
    athletes_size_df = athletes_df[['Height', 'Weight']].dropna()
    scaler = StandardScaler()
    athletes_size_standardized_df = scaler.fit_transform(athletes_size_df)

    # use GaussianMixture on standardized data
    n_components = 2
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(athletes_size_standardized_df)
    athletes_df['Cluster'] = gmm.predict(athletes_size_standardized_df)

    fig = px.scatter(
        athletes_df,
        x='Height',
        y='Weight',
        color='Cluster',
        hover_data={'Height': True, 'Weight': True, 'Cluster': True, 'Sport': True},
        title='GMM Clustering',
        labels={'Height': 'Height', 'Weight': 'Weight', 'Cluster': 'Cluster'}
    )

    return fig

def create_athlete_sex_fig(athletes_df):

    athletes_df['Sex'] = athletes_df['Sex'].map({'M': 1, 'F': 0})
    fig = px.scatter(
        athletes_df,
        x='Height',
        y='Weight',
        color='Sex',
        hover_data={'Height': True, 'Weight': True, 'Sport': True},
        title='GMM Clustering',
        labels={'Height': 'Height', 'Weight': 'Weight', 'Sex': 'Sex'}
    )
    
    return fig
