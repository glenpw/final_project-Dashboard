import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table as dt
import numpy as np
from src.components.dataTitanic import dfMovies, dfGenre, id_map, dfRating, cosine_sim
# from src.components.tab3.callbacks import topchart,genre_chart,metadata_chart

def generate_table(dataframe, pagesize=10):
    return dt.DataTable(
        # id='table-multicol-sorting',
        columns=[
            {"name": i, "id": i} for i in dataframe.columns
        ],
        pagination_settings={
            'current_page': 0,
            'page_size': pagesize
        },
        style_table={'overflowX': 'scroll'},
        pagination_mode='be',
        sorting='be',
        sorting_type='multi',
        sorting_settings=[]
    )

def renderIsiTab3():
    return [
        html.Center([
            html.H2('Movie Recommender', className='title')      
        ]),
        html.Div([
            html.Div([
                html.P('UserID : '),
                # dcc.Input(id='userPredict', type='text', value='',style=dict(width='100%'))
                dcc.Dropdown(
                    id='userPredict',
                    options=[{'label' : i, 'value' : i} for i in dfRating['userId'].unique()],
                    value='All'
                )
            ], className='col-4'),
            html.Div([
                html.P('Pick a Movie : '),
                # dcc.Input(id='moviesPredict', type='text', value='',style=dict(width='100%'))
                dcc.Dropdown(
                    id='moviePredict',
                    options=[{'label' : i, 'value' : i} for i in dfMovies['title'].sort_values()],
                    value='All'
                )
            ], className='col-4'),
            html.Div([
                html.P('Your Favourite Genre : '),
                dcc.Dropdown(
                    id='genrePredict',
                    options=[{'label' : i, 'value' : i} for i in ['Animation','Comedy','Family','Adventure','Fantasy','Romance','Drama','Action','Crime','Thriller','Horror','History','Science Fiction','Mystery','War','Foreign','Music','Documentary','Western','TV Movie']],
                    value='All'
                )
            ], className='col-4'),
        ], className='row'),html.Br(),           
            html.Div([
                html.Div([
                    html.Br(),
                    html.Button("Predict", id='buttonPredict', style=dict(width='100%'))
                ], className='col-4'),
            ], className = 'row'),html.Br(),html.Br(),
        html.Center(id='tableTop'),# children=topchart()),
        # html.H3("Popular Movies"),
        html.Center(id='tableGenre'),# children=genre_chart(genre)),
        # html.H3("Top {} Movies".format('Animation')),
        html.Center(id='tableMeta')#, children = metadata_chart(userId, title)),
    ]


        # html.H3("Top Picks For You"),
        # html.Center(metadata_chart(userId = 1, title = 'Interstellar')),
        # html.H3("Popular Movies"),
        # html.Center(topchart()),
        # html.H3("Top {} Movies".format('Animation')),
        # html.Center(genre_chart(genre = 'Animation')),