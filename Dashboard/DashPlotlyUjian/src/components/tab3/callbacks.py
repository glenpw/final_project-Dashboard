import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table as dt
import numpy as np
from src.components.dataTitanic import dfMovies, dfGenre, id_map, dfRating, cosine_sim
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from surprise import Reader, Dataset, SVD, evaluate

def topchart():
    vote_counts = dfMovies[dfMovies['vote_count'].notnull()]['vote_count'].astype('int')
    m = vote_counts.quantile(0.95)
    vote_averages = dfMovies[dfMovies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    dfTopChart = dfMovies[(dfMovies['vote_count'] >= m) & (dfMovies['vote_count'].notnull()) & (dfMovies['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
    def weighted_rating(x):
        v = x['vote_count']
        R = x['vote_average']
        return (v/(v+m) * R) + (m/(m+v) * C)
    dfTopChart['weighted_rate'] = dfTopChart.apply(weighted_rating, axis=1)
    dfTopChart = dfTopChart.sort_values('weighted_rate', ascending=False)
    dfTopChart['popularity'] = dfTopChart['popularity'].astype(float)
    dfPopular = dfTopChart.sort_values('popularity',ascending=False)
    dfPopular = dfPopular[['title','year','vote_average','genres']]
    # dfPopular['genres'] = dfPopular['genres'].apply(lambda x: ' ,'.join(map(str, x)))
    dfPopular.columns = ['Title','Year','Rating','Genres']
    return [html.H3("Top Chart"),
        dt.DataTable(
            id='tableTop',
            columns=[{"name": i, "id": i} for i in dfPopular.columns],
            data=dfPopular.head(5).to_dict('records'),
        )]

def genre_chart(genre):
    global dfGenre
    # Bikin DataFrame yg berisi genre yang di input
    # print('TOP 10 {} Movies'.format(genre))
    df = dfGenre[dfGenre['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    # menggunakan rumus IMDB's weighte rating
    C = vote_averages.mean()
    m = vote_counts.quantile(0.95)
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity','genre']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('float')
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    # Sort berdasarkan Weighted Rating
    qualified = qualified.sort_values('wr', ascending=False)
    # genreRecommender('Animation')
    qualified = qualified[['title','year','vote_average']]
    qualified.columns = ['Title','Year','Rating']
    qualified['Genres'] = genre
    return dt.DataTable(
        id='tableGenre',
        columns=[{"name": i, "id": i} for i in qualified.columns],
        data=qualified.head().to_dict('records'),
    )

def metadata_chart(userId, title,genre):
    global dfMovies
    # global id_map
    id_map.set_index('title')
    dfMetadata = dfMovies.reset_index(drop=True)
    # dfMetadata = dfMetadata.reset_index(drop=True)
    # dfMetadata = dfMetadata.reset_index()
    titles = dfMetadata['title']
    indices = pd.Series(dfMetadata.index, index=dfMetadata['title'])
    reader = Reader()
    data = Dataset.load_from_df(dfRating[['userId', 'movieId', 'rating']], reader)
    # # Train data 5 folds
    # # data.split(n_folds=5)
    svd = SVD()
    # # evaluate(svd, data, measures=['RMSE'])
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    # # Ambil index dari movie title
    idx = indices[title]
    # # Cek tmdbId
    tmdbId = id_map[id_map['title'] == title]['id']
    # Cek movieId
    movie_id = id_map[id_map['title'] == title]['movieId']
    # Menghitung similarity score dari semua movie terhadap movie title tersebut
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    # Sort movies berdasarkan similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Ambil similarity score dari 25 movie yang mirip, mulai dari index 1 karna index 0 = film sendiri (sangat similiar)
    sim_scores = sim_scores[1:26]
    # Mendapatkan index movie nya
    movie_indices = [i[0] for i in sim_scores]
    # Buat DataFrame dari id movie_indices
    movies = dfMetadata.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id','genres']]
    # Hitung SVD.est simpan di column 'est' lalu di sort
    # id_map.drop('title')
    def svdmap():
        movid = []
        for x in movies['id']:
            movid.append(id_map[id_map['id'] == x]['movieId'].iloc[0])
        estsvd = []
        for a in movid:
            estsvd.append(svd.predict(userId,a).est)
        return estsvd
    movies['est'] = svdmap()
    # movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, id_map[id_map['id'] == x]['movieId'][0]).est)
    # Sort est / prediksi rating
    movies = movies.sort_values('est', ascending=False)
    # movies['est'] = movies['id'].apply(lambda x : id_map[id_map['id'] == x]['movieId'][0])
    movies = movies[['title','year','vote_average','genres']]
    movies.columns = ['Title','Year','Rating','Genres']
    return [
        html.H3('Top Picks For You')
        ,dt.DataTable(
        id='tableMeta',
        columns=[{"name": i, "id": i} for i in movies.columns],
        data=movies.head(10).to_dict('records'),
    ),html.H3('Top {} Movies'.format(genre)),
    genre_chart(genre)]

def callbackrecommend(n_clicks,userId, title, genre):
    return metadata_chart(userId, title,genre)
