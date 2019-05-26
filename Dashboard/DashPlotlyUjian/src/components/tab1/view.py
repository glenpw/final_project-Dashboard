import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from src.components.dataTitanic import dfTitanicTable

# def generate_table(dataframe, max_row=10):
#     return html.Table(
#         #Header
#         [html.Tr([html.Th(col) for col in dataframe.columns])] +
#         #Body
#         [html.Tr(
#             [html.Td(
#                 str(dataframe.iloc[i][col])) for col in dataframe.columns
#                 ]) for i in range(min(len(dataframe), int(max_row)))]
#     )

def generate_table(dataframe, pagesize=10):
    return dt.DataTable(
        id='table-multicol-sorting',
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

def renderIsiTab1():
    return [
            html.Div([
                html.Div([
                    html.P('Title : '),
                    dcc.Input(id='nameSearch', type='text', value='',style=dict(width='100%'))
                ], className='col-4'),
                html.Div([
                    html.P('Year : '),
                    dcc.Dropdown(
                        id='survivedSearch',
                        options=[{'label' : i, 'value' : i} for i in ['All','2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009','2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001','2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993','1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985','1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977','1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969','1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961','1960', '1959', '1958', '1957', '1956', '1955', '1954', '1953','1952', '1951', '1950', '1949', '1948', '1947', '1946', '1945','1944', '1943', '1942', '1941', '1940', '1939', '1938', '1937','1936', '1935', '1934', '1933', '1932', '1931', '1930', '1929','1928', '1927', '1926', '1925', '1924', '1923', '1922', '1921','1920', '1919', '1918', '1917', '1916', '1915', '1902']],
                        value='All'
                    )
                ], className='col-4'),
                html.Div([
                    html.P('Genre : '),
                    dcc.Dropdown(
                        id='genreSearch',
                        options=[{'label' : i, 'value' : i} for i in ['All','Animation','Comedy','Family','Adventure','Fantasy','Romance','Drama','Action','Crime','Thriller','Horror','History','Science Fiction','Mystery','War','Foreign','Music','Documentary','Western','TV Movie']],
                        value='All'
                    )
                ], className='col-4'),
            ], className='row'),html.Br(),
            html.Div([
                html.Div([
                    html.P('Cast : '),
                    dcc.Input(id='castSearch', type='text', value='',style=dict(width='100%'))
                ], className='col-4'),
                html.Div([
                    html.P('Director : '),
                    dcc.Input(id='directorSearch', type='text', value='',style=dict(width='100%'))
                ], className='col-4'),
            ], className='row'),html.Br(),           
            html.Div([
                html.Div([
                    html.P('Ratings : '),
                    dcc.RangeSlider(
                        marks={i: str(i) for i in range(0, 11)},
                        min=dfTitanicTable['Rating'].min(),
                        max=dfTitanicTable['Rating'].max(),
                        value=[dfTitanicTable['Rating'].min(),dfTitanicTable['Rating'].max()],
                        className='rangeslider',
                        id='totalSearch'
                    ),
                ], className='col-10'),
                    html.Div([
                        html.Br(),
                        html.Button('Search', id='buttonsearch', style=dict(width='100%'))
                    ], className='col-2'),
            ], className = 'row'),html.Br(),html.Br(),
            html.Div([
                html.P('Max Row : '),
                dcc.Input(id='rowMax', value=10, type='number', max=len(dfTitanicTable))
            ], className='col-'),
            html.Center([
                html.H2('Movie Dataset', className='title')      
            ]),
            html.Center(id='tableData', children=generate_table(dfTitanicTable))
        ]