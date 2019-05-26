import requests
import pandas as pd

from src.components.tab1.view import generate_table
from src.components.dataTitanic import dfTitanicTable

def callbacksortingtable(pagination_settings, sorting_settings):
    # print(sorting_settings)
    if len(sorting_settings):
        dff = dfTitanicTable.sort_values(
            [col['column_id'] for col in sorting_settings],
            ascending=[
                col['direction'] == 'asc'
                for col in sorting_settings
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = dfTitanicTable

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

def callbackfiltertable(n_clicks,maxrows,name,survive,genre,vote,cast,direc):
    global dfTitanicTable
    dfTitanicTable = pd.read_csv('dfTable.csv')

    dfFilter = dfTitanicTable[((dfTitanicTable['Rating'] >= vote[0]) & (dfTitanicTable['Rating'] <= vote[1]))]
    if(survive == 'All'):
        dfTitanicTable = dfFilter
    else:
        dfTitanicTable = dfFilter[dfFilter['Year'] == int(survive)]
    if(genre =='All'):
        dfTitanicTable = dfTitanicTable
    else:
        dfTitanicTable = dfTitanicTable[dfTitanicTable['Genres'].str.contains(str(genre),na=False)]
    if(name == ''):
        dfTitanicTable = dfTitanicTable
    else:
        dfTitanicTable = dfTitanicTable[dfTitanicTable['Title'].str.contains(str(name),na=False)]
    if(cast == ''):
        dfTitanicTable = dfTitanicTable
    else:
        dfTitanicTable = dfTitanicTable[dfTitanicTable['Cast'].str.contains(str.lower(cast).replace(' ', ''),na=False)]
    if(direc == ''):
        dfTitanicTable = dfTitanicTable
    else:
        dfTitanicTable = dfTitanicTable[dfTitanicTable['Director'].str.contains(str.lower(direc).replace(' ', ''),na=False)]
    return generate_table(dfTitanicTable, pagesize=maxrows)