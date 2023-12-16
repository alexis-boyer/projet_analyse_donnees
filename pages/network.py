from dash import html, dcc
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from math import sqrt

MIN_WEIGHT = 200
MAX_THICKNESS = 3

def create_layout(data) -> html.Div:
    G, pos = create_contry_podium_graph(data["df_athlete"])
    louvain_communities_graph_pyplot(G, pos)
    return html.Div([
        html.H2('Network'),
        dcc.Graph(figure=simple_graph_pyplot(G, pos)),
        dcc.Graph(figure=degree_graph_pyplot(G, pos)),
        dcc.Graph(figure=closeness_graph_pyplot(G, pos)),
        dcc.Graph(figure=louvain_communities_graph_pyplot(G, pos))
    ])

def create_contry_podium_graph(athletes_df):
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

    return G, pos

def simple_graph_pyplot(G, pos):
    edge_x = []
    edge_y = []
    weight = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append((x0, x1))
        edge_y.append((y0, y1))
        weight.append(G.get_edge_data(edge[0], edge[1])['weight'])

    max_weight = max(weight)
    thickness = [ MAX_THICKNESS*(x / max_weight) for x in weight ]

    edge_trace = []

    for i in range(len(edge_x)):
        edge_trace.append(
            go.Scatter(
                x=edge_x[i], y=edge_y[i],
                line=dict(width=thickness[i], color='#888'),
                hoverinfo='none',
                mode='lines')
        )
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color = '#ff0000',
            size=10,
            line_width=2))

    node_trace.text = list(G.nodes())

    fig = go.Figure(data=edge_trace + [node_trace],
             layout=go.Layout(
                title='Countries network by shared podiums on 1968 games',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    
    return fig

def degree_graph_pyplot(G, pos):
    edge_x = []
    edge_y = []
    weight = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append((x0, x1))
        edge_y.append((y0, y1))
        weight.append(G.get_edge_data(edge[0], edge[1])['weight'])

    max_weight = max(weight)
    thickness = [ MAX_THICKNESS*(x / max_weight) for x in weight ]

    edge_trace = []

    for i in range(len(edge_x)):
        edge_trace.append(
            go.Scatter(
                x=edge_x[i], y=edge_y[i],
                line=dict(width=thickness[i], color='#888'),
                hoverinfo='none',
                mode='lines')
        )
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Degree',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_text = list(G.nodes())

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=edge_trace + [node_trace],
             layout=go.Layout(
                title='Countries network by shared podiums on 1968 games with nodes degree',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    
    return fig

def closeness_graph_pyplot(G, pos):
    edge_x = []
    edge_y = []
    weight = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append((x0, x1))
        edge_y.append((y0, y1))
        weight.append(G.get_edge_data(edge[0], edge[1])['weight'])

    max_weight = max(weight)
    thickness = [ MAX_THICKNESS*(x / max_weight) for x in weight ]

    edge_trace = []

    for i in range(len(edge_x)):
        edge_trace.append(
            go.Scatter(
                x=edge_x[i], y=edge_y[i],
                line=dict(width=thickness[i], color='#888'),
                hoverinfo='none',
                mode='lines')
        )
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Closeness Centrality',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_trace.marker.color = list(nx.closeness_centrality(G).values())
    node_trace.text = list(G.nodes())

    fig = go.Figure(data=edge_trace + [node_trace],
             layout=go.Layout(
                title='Countries network by shared podiums on 1968 games with nodes closeness centrality',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    
    return fig

def louvain_communities_graph_pyplot(G, pos):
    edge_x = []
    edge_y = []
    weight = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append((x0, x1))
        edge_y.append((y0, y1))
        weight.append(G.get_edge_data(edge[0], edge[1])['weight'])

    max_weight = max(weight)
    thickness = [ MAX_THICKNESS*(x / max_weight) for x in weight ]

    edge_trace = []

    for i in range(len(edge_x)):
        edge_trace.append(
            go.Scatter(
                x=edge_x[i], y=edge_y[i],
                line=dict(width=thickness[i], color='#888'),
                hoverinfo='none',
                mode='lines')
        )
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Community',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    communities = nx.community.louvain_communities(G)

    color = [-1 for x in G.nodes()]
    i = 0
    for community in communities:
        for node in community:
            color[list(G.nodes()).index(node)] = i
        i += 1


    node_trace.marker.color = color
    node_trace.text = list(G.nodes())

    fig = go.Figure(data=edge_trace + [node_trace],
             layout=go.Layout(
                title='Countries network by shared podiums on 1968 games with community',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    
    return fig
