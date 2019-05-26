import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from src.components.dataTitanic import dfUserRating

# def generate_table(dataframe, pagesize=10):
#     return dt.DataTable(
#         # id='table-multicol-sorting1',
#         columns=[
#             {"name": i, "id": i} for i in dataframe.columns
#         ],
#         pagination_settings={
#             'current_page': 0,
#             'page_size': pagesize
#         },
#         style_table={'overflowX': 'scroll'},
#         pagination_mode='be',
#         sorting='be',
#         sorting_type='multi',
#         sorting_settings=[]
#     )

def renderIsiTab4():
    return [
            html.Div([
                 html.Div([
                    html.P('UserID : '),
                    # dcc.Input(id='userPredict', type='text', value='',style=dict(width='100%'))
                    dcc.Dropdown(
                        id='userHist',
                        options=[{'label' : i, 'value' : i} for i in dfUserRating['userId'].unique()],
                        value=''
                    )
                ], className='col-2')
            ], className='row'),html.Br(),
            html.Div([
                html.Div([
                    html.Button('Search', id='buttonsearchist', style=dict(width='100%'))
                ], className='col-2'),
            ], className='row'),
            # html.Div([
            #     html.P('Max Row : '),
            #     dcc.Input(id='rowMaxHist', value=10, type='number', max=len(dfUserRating))
            # ], className='col-'),
            html.Center([
                html.H3('User Rating History', className='title')      
            ]),
            html.Center(id='tableDataHist')
        ]