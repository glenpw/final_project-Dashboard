import dash_core_components as dcc
import dash_html_components as html
from src.components.dataTitanic import dfMovies, dfGenre
import plotly.graph_objs as go

def renderIsiTab2():
    return [
        dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x= dfMovies['year'].value_counts().sort_index().index,
                    y=dfMovies['year'].value_counts().sort_index().values,
                    # name='Rest of world',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                ),
            ],
            layout=go.Layout(
                title='Movie Release Year',
                # showlegend=True,
                # legend=go.layout.Legend(
                #     x=0,
                #     y=1.0
                # ),
                # margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 500},
        id='categoryGraph'
    ),
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x= dfMovies['vote_average'].value_counts().sort_index().index,
                    y=dfMovies['vote_average'].value_counts().sort_index().values,
                    # name='Rest of world',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                ),
            ],
            layout=go.Layout(
                title='Movie Rating Average',
                # showlegend=True,
                # legend=go.layout.Legend(
                #     x=0,
                #     y=1.0
                # ),
                # margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 500},
        # id='categoryGraph'
    ),
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x= dfGenre['genre'].value_counts().sort_index().index,
                    y=dfGenre['genre'].value_counts().sort_index().values,
                    # name='Rest of world',
                    marker=go.bar.Marker(
                        color='rgb(55, 83, 109)'
                    )
                ),
            ],
            layout=go.Layout(
                title='Movie Genres',
                # showlegend=True,
                # legend=go.layout.Legend(
                #     x=0,
                #     y=1.0
                # ),
                # margin=go.layout.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 500},
        # id='categoryGraph'
    )
    ]