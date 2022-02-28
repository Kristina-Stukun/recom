import numpy as np
import pandas as pd

#считываем данные таблиц
history = pd.read_csv("history.csv")
movies= pd.read_csv("movies.csv")

#объединяем данные по id фильма (матрица просмотров)
movie_data = pd.merge(history, movies, on='MovieID')

#определяем интересные жанры для пользователя
join_data = movie_data.groupby(['UserID'])['ListOfGenres'].apply('|'.join).reset_index(name='ListOfGenres')

#предположим, что ищем рекомендации для конкретного пользователя с id=1
id_us=1
filter_data= join_data.loc[join_data['UserID'] == id_us]

#берем 5 наиболее просматриваемых жанров пользователям
items = pd.Series(filter_data['ListOfGenres'][0].split('|')).value_counts(sort=True)
genre_unique = pd.DataFrame(items)
genre_unique = genre_unique.reset_index()
genre_unique.columns = ['genre', 'count']
genre_unique = genre_unique['genre'].head()
print("Пользователю с id = ", id_us, "нравятся такие жанры: ", genre_unique)

#получаем таблицы всех фильмов + рейтинг просмотров
data_rating = movie_data.groupby('MovieID')['Rating'].mean()
all_movie = pd.merge(data_rating, movies,how = 'right', on='MovieID')
all_movie=all_movie.fillna(0) 

q=pd.merge(history.loc[history['UserID']==id_us], movies, on= 'MovieID')

print("Он посмотрел фильмы: ",q['Title'])

#ищем все фильмы с данными жанрами и отсеиваем по рейтингу >4, чтобы рекомендовать только хорошие 
all_movie=all_movie.loc[all_movie['Rating']>=4.0]
dt=pd.DataFrame()
for i in genre_unique:
    dt=pd.concat([dt, all_movie[all_movie['ListOfGenres'].str.contains(i)]],ignore_index=True)
dt2=dt.copy()
dt2.drop_duplicates(subset=['MovieID'],keep='first',inplace=True)
dt2=dt2[['Title','Rating','MovieID']]
#отсеиваем просмотренные 
history_user = history.loc[history['UserID']==id_us]['MovieID']
x= list(history_user)
dt2 = dt2.loc[~dt2['MovieID'].isin(x)]
print("Ему можно рекомендовать такие фильмы: ", dt2[['Title', 'Rating']])