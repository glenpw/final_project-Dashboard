import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from src.components.dataTitanic import dfMovies
from src.components.tab1.view import renderIsiTab1
from src.components.tab2.view import renderIsiTab2
from src.components.tab3.view import renderIsiTab3
from src.components.tab4.view import renderIsiTab4

from src.components.tab1.callbacks import callbacksortingtable, callbackfiltertable
from src.components.tab2.callbacks import callbackupdatecatgraph
from src.components.tab3.callbacks import topchart, genre_chart, metadata_chart, callbackrecommend
from src.components.tab4.callbacks import callbackfiltertablehistory


app = dash.Dash(__name__)
server = app.server

app.title = 'Dashboard Movie Recommender System'

app.layout = html.Div([
    html.H1('Dashboard Movie Recommender System',style={'color': '#000080'}),
    html.H4('Created by Glen P. Wangsa'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Data Movies', value='tab-1', children=renderIsiTab1()),
        dcc.Tab(label='Plots', value='tab-2', children=renderIsiTab2()),
        dcc.Tab(label='Recommender System', value='tab-3', children=renderIsiTab3()),
        dcc.Tab(label='User History', value='tab-4', children=renderIsiTab4())
    ],
    style={'fontFamily': 'Arial'},
    content_style={
        'fontFamily' : 'system-ui',
        'borderBottom' : '1px solid #d6d6d6',
        'borderLeft' : '1px solid #d6d6d6',
        'borderRight' : '1px solid #d6d6d6',
        'padding' : '50px'
    })],
    style={
        'maxWidth' : '1200px',
        'margin' : '0 auto'
    }
)

# ______________CALLBACK TABLE________________
@app.callback(
    Output('table-multicol-sorting', "data"),
    [Input('table-multicol-sorting', "pagination_settings"),
     Input('table-multicol-sorting', "sorting_settings")])
def update_sort_paging_table(pagination_settings, sorting_settings):
    return callbacksortingtable(pagination_settings, sorting_settings)

@app.callback(
    Output(component_id='tableData', component_property='children'),
    [Input(component_id='buttonsearch', component_property='n_clicks'),
    Input(component_id='rowMax', component_property='value')],
    [
    State(component_id='nameSearch', component_property='value'),
    State(component_id='survivedSearch', component_property='value'),
    State(component_id='genreSearch', component_property='value'),
    State(component_id='totalSearch', component_property='value'),
    State(component_id='castSearch', component_property='value'),
    State(component_id='directorSearch', component_property='value')]
)
def update_table(n_clicks,maxrows,name,survive,genre,vote,cast,direc):
    return callbackfiltertable(n_clicks,maxrows,name,survive,genre,vote,cast,direc)

# ________________CALLBACK PLOT________________
# @app.callback(
#     Output(component_id='categoryGraph', component_property='figure'),
#     [
#         Input(component_id='jenisplotcategory', component_property='value'),
#         Input(component_id='xplotcategory', component_property='value'),
#         Input(component_id='yplotcategory', component_property='value'),
#         Input(component_id='statsplotcategory', component_property='value')
#     ]
# )
# def update_category_graph(jenisPlot,xPlot,yPlot,stats):
#     return callbackupdatecatgraph(jenisPlot,xPlot,yPlot,stats)

# __________CALLBACK DISABLE STATS_____________
# @app.callback(
#     Output(component_id='statsplotcategory', component_property='disabled'),
#     [Input(component_id='jenisplotcategory', component_property='value')]
# )
# def update_disable_stats(jenisPlot):
#     if (jenisPlot == 'Bar'):
#         return False
#     return True

# ___ CALLBACK PREDICT
@app.callback(
    Output(component_id='tableTop', component_property='children'),
    # Output(component_id='tableGenre', component_property='children'),
    # Output(component_id='tableMeta', component_property='children'),
    [Input(component_id='buttonPredict', component_property='n_clicks')],
    [
    State(component_id='userPredict', component_property='value'),
    State(component_id='moviePredict', component_property='value'),
    State(component_id='genrePredict', component_property='value')
    ]
)
def update_predict(n_clicks,userId, title, genre):
    return callbackrecommend(n_clicks,userId, title, genre)

# ____ CALLBACK HIST

# @app.callback(
#     Output('table-multicol-sorting', "data"),
#     [Input('table-multicol-sorting', "pagination_settings"),
#      Input('table-multicol-sorting', "sorting_settings")])
# def update_sort_paging_table(pagination_settings, sorting_settings):
#     return callbacksortingtable(pagination_settings, sorting_settings)

@app.callback(
    Output(component_id='tableDataHist', component_property='children'),
    [Input(component_id='buttonsearchist', component_property='n_clicks')],
    [
    # State(component_id='rowMaxHist', component_property='value'),
    State(component_id='userHist', component_property='value')
    ]
    # ,
    # [
    # State(component_id='nameSearch', component_property='value'),
    # State(component_id='survivedSearch', component_property='value'),
    # State(component_id='genreSearch', component_property='value'),
    # State(component_id='totalSearch', component_property='value'),
    # State(component_id='castSearch', component_property='value'),
    # State(component_id='directorSearch', component_property='value')]
)
def update_table_hist(n_clicks,userHist):
    return callbackfiltertablehistory(n_clicks,userHist)

if __name__ == '__main__':
    app.run_server(debug=True)  



