from DataBase import SessionLocal
import requet as query_helpers

# Créer une session
db = SessionLocal()

# %%
# Tester la récupération de films
movies = query_helpers.get_movies(db, limit=5, genre="Comedy")

for movie in movies:
    print(f"ID: {movie.movieId}, Titre: {movie.title}, Genres: {movie.genres}")


# %% 

get = query_helpers.get_movie_count(db)
tag = query_helpers.get_tag_count(db)
print(tag)
print(get)

# %%
# Fermer la session
db.close()