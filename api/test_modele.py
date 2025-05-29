#%%
from DataBase import SessionLocal

#%%
db = SessionLocal()
# %%
from modele import Tag
# %%
from modele import Movie

# %%
from modele import Rating

# %%
from modele import Link


# %%
high_rated_movies = (
    db.query(Movie, Rating)
    .join(Rating)
    .filter(Rating.rating >= 4)
    .limit(5)
    .all()
)

for movie, rating in high_rated_movies:
    print(movie.title, rating.rating)

# %%
hight_rated_movies = (
    db.query(Movie.title, Rating.rating)
    .join(Rating)
    .filter(Rating.rating >= 4, Movie.movieId == Rating.movieId,Movie.genres.like("Action"))
    .limit(5)
    .all()
    
)
print(hight_rated_movies)

for title, rating in hight_rated_movies:
    print(title, rating)
# %%
db.close()