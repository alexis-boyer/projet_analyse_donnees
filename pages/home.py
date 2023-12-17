import dash
from dash import html

def create_layout() -> html.Div:
    return html.Div(className='home-container', children=[
        html.Div(className='home-header', children=[
            html.Div(className='home-header-content', children=[
                html.H1(className='home-title', children='Data analysis of Olympic Athletes since 1896'),
                html.H3(className='home-subtitle', children='By TREMBLEAU Thibault, BRUSTOLIN Lucas and BOYER Alexis'),
                html.P(className='home-paragraph', children=
                    'This website made in Dash is an analysis of a Dataset listing all the Olympic Athletes and their events since 1896. If you click on the tabs on the left, you will be able to see graphs and statistics about the data.'
                ),
                html.P(className='home-paragraph', children=
                    'You can also click on the buttons below to see from where the dataset is coming from and the Github repository of this project with further information in the README.'
                ),
                html.Div(className='home-buttons', children=[
                    html.A(
                        className='button-link',
                        href='https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results',
                        children='Dataset source',
                        target='_blank'
                    ),
                    html.A(
                        className='button-link',
                        href='https://github.com/alexis-boyer/projet_analyse_donnees',
                        children='Github repository',
                        target='_blank'
                    )
                ])
            ]),
            html.Div(className='home-header-image', children=[
                html.Img(src='assets/olympic_games_illustration.png', alt='Olympic Games Illustration')
            ])
        ]),
        html.Div(className='home-section', children=[
            html.P(className="paragraph", children=[
                'Each row of this dataset corresponds to an athlete competing in a particular Olympic event. Thus, each athlete has one or more rows depending on the number of events they participated in. Each row contains those informations:'
            ]),
            html.Table(className='home-table', children=[
                html.Tr(className='home-table-top-row', children=[
                    html.Th(),
                    html.Th('Description'),
                    html.Th('Examples', colSpan=2)
                ]),
                html.Tr([
                    html.Th('ID'),
                    html.Td('Unique number for each athlete'),
                    html.Td('14359'),
                    html.Td('367')
                ]),
                html.Tr([
                    html.Th('Name'),
                    html.Td('Athlete\'s name'),
                    html.Td('Marine Clmence Boyer'),
                    html.Td('Masashi Abe')
                ]),
                html.Tr([
                    html.Th('Sex'),
                    html.Td('M or F'),
                    html.Td('F'),
                    html.Td('M')
                ]),
                html.Tr([
                    html.Th('Age'),
                    html.Td('Integer'),
                    html.Td('16'),
                    html.Td('28')
                ]),
                html.Tr([
                    html.Th('Height'),
                    html.Td('In centimeters'),
                    html.Td('162'),
                    html.Td('175')
                ]),
                html.Tr([
                    html.Th('Weight'),
                    html.Td('In kilograms'),
                    html.Td('52'),
                    html.Td('64')
                ]),
                html.Tr([
                    html.Th('Team'),
                    html.Td('Team name'),
                    html.Td('France'),
                    html.Td('Japan')
                ]),
                html.Tr([
                    html.Th('NOC'),
                    html.Td('National Olympic Committee 3-letter code'),
                    html.Td('FRA'),
                    html.Td('JPN')
                ]),
                html.Tr([
                    html.Th('Games'),
                    html.Td('Year and season'),
                    html.Td('2016 Summer'),
                    html.Td('1994 Winter')
                ]),
                html.Tr([
                    html.Th('Year'),
                    html.Td('Integer'),
                    html.Td('2016'),
                    html.Td('1994')
                ]),
                html.Tr([
                    html.Th('Season'),
                    html.Td('Summer or Winter'),
                    html.Td('Summer'),
                    html.Td('Winter')
                ]),
                html.Tr([
                    html.Th('City'),
                    html.Td('Host city'),
                    html.Td('Rio de Janeiro'),
                    html.Td('Lillehammer')
                ]),
                html.Tr([
                    html.Th('Sport'),
                    html.Td('Sport'),
                    html.Td('Gymnastics'),
                    html.Td('Nordic Combined')
                ]),
                html.Tr([
                    html.Th('Event'),
                    html.Td('Event'),
                    html.Td('Gymnastics Women\'s Team All-Around'),
                    html.Td('Nordic Combined Men\'s Team')
                ]),
                html.Tr([
                    html.Th('Medal'),
                    html.Td('Gold, Silver, Bronze, or NA'),
                    html.Td('NA'),
                    html.Td('Gold')
                ])
            ])
        ])
    ])
