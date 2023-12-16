from dash import html, dcc
import networkx as nx
import matplotlib.pyplot as plt
from math import sqrt

MIN_WEIGHT = 500

def create_layout(data) -> html.Div:
    fig = create_contry_podium_network(data['df_athlete'])
    return html.Div([
        html.H2('Network'),
        dcc.Graph(figure = fig),
    ])

def create_contry_podium_network(athletes_df):
    # Create a directed graph
    G = nx.Graph()

    # Iterate through each row in the dataframe
    data_df = athletes_df[(athletes_df['Year'] == 1968)].dropna(subset=['Medal'])
    for index, row in data_df.iterrows():
        id1 = row['ID']
        country1 = row['NOC']
        year = row['Year']
        sport = row['Sport']
        medal = row['Medal']

        # Check if the medal is not 'NA'
        if medal:
            # Find other countries that won a medal in the same year and sport
            same_year_sport = data_df[(data_df['Year'] == year) & (data_df['Sport'] == sport) & 
                                            (data_df['ID'] != id1) & (data_df['NOC'] != country1)]

            # Add edges between the current country and other countries in the same year and sport
            for _, other_row in same_year_sport.iterrows():
                country2 = other_row['NOC']
                if country1 != country2:
                    if G.has_edge(country1, country2):
                        G[country1][country2]['weight'] += 1
                    else:
                        G.add_edge(country1, country2, weight=1)

    edges_to_remove = [(u, v) for u, v, data in G.edges(data=True) if 'weight' in data and data['weight'] < MIN_WEIGHT]
    for u, v in edges_to_remove:
        G.remove_edge(u, v)
    
    # Find isolated nodes (nodes with degree 0)
    isolated_nodes = [node for node, degree in G.degree() if degree == 0]

    # Remove isolated nodes from the graph
    G.remove_nodes_from(isolated_nodes)

    # pos
    pos = nx.spring_layout(G, seed=7, k=5/sqrt(G.order()), scale=3)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1500)

    # edges
    nx.draw_networkx_edges(G, pos, width=6)

    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()