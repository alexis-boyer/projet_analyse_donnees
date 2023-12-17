from dash import html, dcc
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
import plotly.express as px


def create_layout(data) -> html.Div:
    figGMM = create_cluster_height_weight(data['df_athlete'])
    figSex = create_athlete_sex_fig(data['df_athlete'])
    figCouuntry = create_medal_country_fig(data['df_athlete'])
    figGMMCountry = create_medal_country_cluster(data['df_athlete'])
    return html.Div([
        html.H2(children='Cluster'),
        html.H3(children='Homme/Femme'),
        dcc.Graph(figure = figGMM),
        dcc.Graph(figure = figSex),
        html.H3(children='Medail remporté'),
        dcc.Graph(figure = figCouuntry),
        dcc.Graph(figure = figGMMCountry)
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
        title='Man/Woman Size',
        labels={'Height': 'Height', 'Weight': 'Weight', 'Sex': 'Sex'}
    )
    
    return fig

def create_medal_country_fig(athletes_df):

    # group data for count
    athletes_grouped_df = athletes_df.groupby(['NOC', 'Year', 'Medal']).size().unstack(fill_value=0).reset_index()
    athletes_grouped_df['Total_Medals'] = athletes_grouped_df[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    athletes_grouped_df = athletes_grouped_df[['NOC', 'Year', 'Total_Medals']]
    
    fig = px.scatter(
        athletes_grouped_df,
        x='Year',
        y='Total_Medals',
        hover_data={'Year': True, 'Total_Medals': True, 'NOC': True},
        title='Medals Won by Country and Year',
        labels={'Year': 'Year', 'Total_Medals': 'Total Medals', 'NOC': 'Country'}
    )

    return fig


def create_medal_country_cluster(athletes_df):

    # group data for count
    athletes_grouped_df = athletes_df.groupby(['NOC', 'Year', 'Medal']).size().unstack(fill_value=0).reset_index()
    athletes_grouped_df['Total_Medals'] = athletes_grouped_df[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    athletes_grouped_df = athletes_grouped_df[['NOC', 'Year', 'Total_Medals']]

    # standarization of numerical data
    athletes_grouped_df.dropna()
    athletes_grouped_numerical_df = athletes_grouped_df[['Year', 'Total_Medals']]
    scaler = StandardScaler()
    athletes_grouped_numerical_standardized_df = scaler.fit_transform(athletes_grouped_numerical_df)

    # use GaussianMixture on standardized data
    n_components = 4
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(athletes_grouped_numerical_standardized_df)
    athletes_grouped_df['Cluster'] = gmm.predict(athletes_grouped_numerical_standardized_df)

    fig = px.scatter(
        athletes_grouped_df,
        x='Year',
        y='Total_Medals',
        color = 'Cluster',
        hover_data={'Year': True, 'Total_Medals': True, 'NOC': True},
        title='Medals Won by Country and Year',
        labels={'Year': 'Year', 'Total_Medals': 'Total Medals', 'NOC': 'Country'}
    )

    return fig

def create_all_cluster(athletes_df):

    # group data for count
    athletes_grouped_df = athletes_df.groupby(['NOC', 'Year', 'Medal']).size().unstack(fill_value=0).reset_index()
    athletes_grouped_df['Total_Medals'] = athletes_grouped_df[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    athletes_grouped_df = athletes_grouped_df[['NOC', 'Year', 'Total_Medals']]

    # standarization of numerical data
    athletes_grouped_df.dropna()
    athletes_grouped_numerical_df = athletes_grouped_df[['Year', 'Total_Medals']]
    scaler = StandardScaler()
    athletes_grouped_numerical_standardized_df = scaler.fit_transform(athletes_grouped_numerical_df)

    # use GaussianMixture on standardized data
    n_components = 4
    gmm = GaussianMixture(n_components=n_components, random_state=42)
    gmm.fit(athletes_grouped_numerical_standardized_df)
    athletes_grouped_df['Cluster'] = gmm.predict(athletes_grouped_numerical_standardized_df)

    fig = px.scatter(
        athletes_grouped_df,
        x='Year',
        y='Total_Medals',
        color = 'Cluster',
        hover_data={'Year': True, 'Total_Medals': True, 'NOC': True},
        title='Medals Won by Country and Year',
        labels={'Year': 'Year', 'Total_Medals': 'Total Medals', 'NOC': 'Country'}
    )

    return fig