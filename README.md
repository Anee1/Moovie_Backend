# Moovie_Backend

# Objectif du projet :
Construire un écosystème data moderne centré sur le cinéma, en partant de fichiers bruts jusqu’à la mise en place d’une API et d’un SDK Python. Ce projet est structuré en plusieurs phases. Cette première phase se concentre sur l’architecture backend et l’exposition des données via une API REST.



# **Contexte**  

Dans ce projet fictif, une entreprise nommée babyCiné souhaite valoriser ses données de films (notes, tags, utilisateurs) afin de mieux servir les cinéphiles, plateformes de streaming et studios.

Les données disponibles sont désorganisées (CSV dispersés, absence de base unifiée).
Mon rôle : en tant que Développeur Backend et Architecte API, structurer, centraliser et exposer ces données via une API performante, sécurisée et facilement réutilisable.



---

## **🔧Travaux réalisés – Phase 1**  

![](architecture.png)

**Objectif : Construire une API robuste pour centraliser et exposer les données MovieLens.**  

 **Design de la base de données** :  
- Modéliser la base de données en SQL à partir des fichiers CSV.  
- Utiliser **SQLite** pour stocker les données de manière efficace.  
- Gérer les relations entre les films, les utilisateurs, les notes et les tags.  

 **Développement de l’API avec FastAPI** :  
- Concevoir un **API RESTful** permettant d'interroger facilement les films et les notes des utilisateurs.  
- Intégrer **Pydantic** pour la validation des données entrantes.  
- Utiliser **SQLAlchemy** pour la gestion des requêtes à la base de données.  

 **Déploiement de l’API** :  
- Héberger l’API sur un cloud public (**Render, AWS, Azure, GCP**).  
- Prévoir une version **on-premise** avec Docker.  
- Sécuriser les endpoints et optimiser les performances.  

 **Création d’un SDK en Python** :  
- Développer un **package Python** permettant aux utilisateurs d'interagir facilement avec l’API.  
- Publier ce package sur **PyPI**, afin qu’il puisse être utilisé dans d'autres projets.  

**Livrables** :  
- Une base de données centralisée et prête à l’emploi.  
- Une API FastAPI documentée et déployée. (https://moovie-backend-1.onrender.com) 
- Un SDK Python simple d'utilisation et bien documenté (https://pypi.org/project/filmAneesdk/)

---







### Compétences clés que vous avez acquises

-  Conception de bases de données relationnelles
-  ORM avec SQLAlchemy
-  Architecture API RESTful avec FastAPI
-  Validation et typage fort avec Pydantic
-  Utilisation de Docker pour contenairiser votre application
-  Déploiement cloud sur Render
-  Génération de documentation API automatique (Swagger / Redoc)
-  Packaging Python, publication sur PyPI, gestion de versions
-  Création d’un SDK professionnel

--- 


