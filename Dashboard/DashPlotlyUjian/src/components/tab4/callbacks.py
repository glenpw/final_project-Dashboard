import requests
import pandas as pd
import dash_table as dt

from src.components.tab1.view import generate_table
from src.components.dataTitanic import dfUserRating

# def callbacksortingtablehist(pagination_settings, sorting_settings):
#     # print(sorting_settings)
#     if len(sorting_settings):
#         dff = dfUserRating.sort_values(
#             [col['column_id'] for col in sorting_settings],
#             ascending=[
#                 col['direction'] == 'asc'
#                 for col in sorting_settings
#             ],
#             inplace=False
#         )
#     else:
#         # No sort is applied
#         dff = dfUserRating

#     return dff.iloc[
#         pagination_settings['current_page']*pagination_settings['page_size']:
#         (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
#     ].to_dict('rows')

def historydf(n_clicks,userHist):
    global dfUserRating
    # dfUserRating = pd.read_csv('dfUserRating.csv')
    dfFilterH = dfUserRating[dfUserRating['userId'] == int(userHist)]
    return[
        dt.DataTable(
        id='tableDataHist',
        columns=[{"name": i, "id": i} for i in dfFilterH.columns],
        data=dfFilterH.to_dict('records'),
    )]

def callbackfiltertablehistory(n_clicks,userHist):
    return historydf(n_clicks,userHist)
