from fastapi import FastAPI, Depends, HTTPException, Query , Path
from sqlalchemy.orm import Session
from typing import List,Optional
from DataBase import SessionLocal
import requet as req
import shema

description = description = """
### 🎬 **Bienvenue dans l'API Film**

Cette API vous permet d'interagir avec la base de données **MovieLens** inspirée du célèbre jeu de données [MovieLens](https://grouplens.org/datasets/movielens/) , une base riche en informations sur les **films**, les **utilisateurs** et leurs **évaluations**.  
Elle expose plusieurs *endpoints REST* permettant de **consulter, filtrer et analyser** les films, évaluations, tags et autres métadonnées.

---

### 🔧 Fonctionnalités principales :
-  Obtenez les détails d’un film à partir de son ID  
-  Recherchez une liste de films avec filtres par titre ou genre  
-  Consultez la note attribuée par un utilisateur à un film spécifique  
-  Filtrez les tags par film ou utilisateur  
-  Explorez les genres, tendances de notation et autres statistiques  

---

### 🧠 Utilisation typique :
-  Développeurs souhaitant intégrer des données cinématographiques dans leurs applications  
-  Data analysts explorant les préférences de visionnage  
-  Chercheurs en machine learning travaillant sur des systèmes de recommandation

---
### Bon à savoir
- Vous pouvez tester tous les endpoints directement via l'interface Swagger "/docs".
- Pour toute erreur (ex : ID inexistant), une réponse claire est retournée avec le bon code HTTP.
"""



app = FastAPI(
    title="Film",
    description= description ,
    version= '0.1')

# --- Dépendance pour la session de la base de donnée ---#

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
       db.close()


# Endpoint pour tester l'API #
@app.get(
 "/",
 summary="Vérifie si l'API MovieLens fonctionne",
 description="""
 Ce point d'entrée permet de vérifier si l'API MovieLens est
opérationnelle. 
 """,
 response_description="Un message de confirmation si l'API fonctionne correctement.",
 operation_id="health_check_movies_api",
 tags=["Verification"],
)
async def root():
 return {"message": "API MovieLens opérationnelle"}


# Endpoint pour recuperer un film à partie de son ID #

@app.get(
   "/film/{filmId}",
   summary="detaille du film",
   description="Récupère les informations détaillées d’un film à partir de son identifiant unique.",
   response_description="Informations détaillées du film",
   response_model= shema.MovieDetailed,
   tags=['film']
)

async def get_film(filmId: int = Path(..., title="ID du film", description="Identifiant unique du film"),db: Session = Depends(get_db)):
   film = req.get_movie(db , filmId)
   if film is None:
      raise HTTPException(status_code=404,detail=f"Aucun film trouvé avec l'ID {filmId}")
   return film


# Endpoint pour obtenir une liste des films (avec pagination et filtres facultatifs title, genre, skip, limit)
@app.get(
    "/films",
    summary="Lister les films",
    description="Retourne une liste de films avec pagination et filtres optionnels par titre ou genre.",
    response_description="Liste de films",
    response_model=List[shema.MovieSimple],
    tags=["films"],
)
def list_movies(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    title: str = Query(None, description="Filtre par titre"),
    genre: str = Query(None, description="Filtre par genre"),
    db: Session = Depends(get_db)
):
    film = req.get_movies(db, skip=skip, limit=limit, title=title, genre=genre)
    return film


# Endpoint pour obtenir une évaluation par utilisateur et film
@app.get(
    "/ratings/{user_id}/{film_id}",
    summary="Obtenir une évaluation par utilisateur et film",
    description="Retourne l'évaluation d'un utilisateur pour un film donné.",
    response_description="Détails de l'évaluation",
    response_model=shema.RatingSimple,
    tags=["évaluations"],
)
def rating(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    film_id: int = Path(..., description="ID du film"),
    db: Session = Depends(get_db)
):
    rating = req.get_rating(db, user_id=user_id, movie_id=film_id)
    if rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune évaluation trouvée pour l'utilisateur {user_id} et le film {film_id}"
        )
    return rating


# Endpoint pour obtenir une liste d’évaluations avec filtres
@app.get(
    "/ratings",
    summary="Lister les évaluations",
    description="Retourne une liste d’évaluations avec pagination et filtres optionnels (film, utilisateur, note min).",
    response_description="Liste des évaluations",
    response_model=List[shema.RatingSimple],
    tags=["évaluations"],
)
def list_ratings(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    movie_id: Optional[int] = Query(None, description="Filtrer par ID de film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID d'utilisateur"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Filtrer les notes supérieures ou égales à cette valeur"),
    db: Session = Depends(get_db)
):
    ratings = req.get_ratings(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id, min_rating=min_rating)
    return ratings


#  Endpoint pour retourner un tag pour un utilisateur et un film donnés, avec le texte du tag
@app.get(
    "/tags/{user_id}/{movie_id}/{tag_text}",
    summary="Obtenir un tag spécifique",
    description="Retourne un tag pour un utilisateur et un film donnés, avec le texte du tag.",
    response_model= shema.TagSimple,
    tags=["tags"],
)
def read_tag(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    tag_text: str = Path(..., description="Contenu exact du tag"),
    db: Session = Depends(get_db)
):
    result = req.get_tag(db, user_id=user_id, movie_id=movie_id, tag_text=tag_text)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tag non trouvé pour l'utilisateur {user_id}, le film {movie_id} et le tag '{tag_text}'"
        )
    return result



# Endpoint pour retourner une liste de tags avec pagination et filtres facultatifs par utilisateur ou film
@app.get(
    "/tags",
    summary="Lister les tags",
    description="Retourne une liste de tags avec pagination et filtres facultatifs par utilisateur ou film.",
    response_model=List[shema.TagSimple],
    tags=["tags"],
)
def list_tags(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    movie_id: Optional[int] = Query(None, description="Filtrer par ID de film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID d'utilisateur"),
    db: Session = Depends(get_db)
):
    return req.get_tags(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id)

# Endpoint pour retourner les identifiants IMDB et TMDB pour un film donné
@app.get(
    "/links/{movie_id}",
    summary="Obtenir le lien d'un film",
    description="Retourne les identifiants IMDB et TMDB pour un film donné.",
    response_model=shema.LinkSimple,
    tags=["links"],
)
def read_link(
    movie_id: int = Path(..., description="ID du film"),
    db: Session = Depends(get_db)
):
    result = req.get_link(db, movie_id=movie_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucun lien trouvé pour le film avec l'ID {movie_id}"
        )
    return result


# Endpoint pour retourner une liste paginée des identifiants IMDB et TMDB de tous les films
@app.get(
    "/links",
    summary="Lister les liens des films",
    description="Retourne une liste paginée des identifiants IMDB et TMDB de tous les films.",
    response_model=List[shema.LinkSimple],
    tags=["links"],
)
def list_links(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    db: Session = Depends(get_db)
):
    return req.get_links(db, skip=skip, limit=limit)


# Endpoint pour obtenir des statistiques sur la base de données
@app.get(
    "/analytics",
    summary="Obtenir des statistiques",
    description="""
    Retourne un résumé analytique de la base de données :

    - Nombre total de films
    - Nombre total d’évaluations
    - Nombre total de tags
    - Nombre de liens vers IMDB/TMDB
    """,
    response_model=shema.AnalyticsResponse,
    tags=["analytics"]
)
def get_analytics(db: Session = Depends(get_db)):
    movie_count = req.get_movie_count(db)
    rating_count = req.get_rating_count(db)
    tag_count = req.get_tag_count(db)
    link_count = req.get_link_count(db)

    return shema.AnalyticsResponse(
        movie_count=movie_count,
        rating_count=rating_count,
        tag_count=tag_count,
        link_count=link_count
    )