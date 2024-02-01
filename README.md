# Crawler Web

## Auteur
AOUACHRI OMAR

## Description
Ce projet implémente un crawler web en Python, conçu pour explorer les pages web à partir d'une URL d'entrée unique. Le crawler est simple, single-threaded, et respecte les règles de politesse.

## Fonctionnalités
- Télécharge les pages web à partir d'une URL d'entrée.
- Respecte les règles de politesse en attendant au moins cinq secondes entre chaque téléchargement.
- Trouve d'autres pages à explorer en analysant les balises de liens dans les documents précédemment explorés.
- S'arrête après avoir exploré 5 liens maximum par page ou lorsque 50 URLs ont été trouvées et téléchargées.
- Écrit les URLs trouvées dans un fichier `crawled_webpages.txt`.
- Vérifie les règles de `robots.txt` pour déterminer si le crawling est autorisé.
- lit le fichier `sitemap.xml` pour réduire le nombre de requêtes aux URLs tout en découvrant plus de pages.
- Respecte la politesse relativement à la vitesse de téléchargement de la dernière page.
- Crée une base de données relationnelle (`pages_web.db`) pour stocker les pages web trouvées ainsi que leur âge.

## Structure du Projet
- `crawler.py`: Contient la classe `Crawler` avec les fonctionnalités principales.
- `main.py`: Fichier principal pour exécuter le crawler.
- `pages_web.db`: Base de données SQLite pour stocker les pages web trouvées.
- `crawled_webpages.txt`: Fichier pour enregistrer les URLs trouvées.

## Utilisation


1. Clonez le dépôt GitHub en utilisant la commande suivante :
   `git clone https://github.com/omaraouachri/Tp1_Omar.git`
   `cd Crawler` 
2. Assurez-vous d'avoir les dépendances requises installées : `requests`, `beautifulsoup4`, `protego`, `sqlite3`
3. Exécutez le fichier `main.py` à la racine du projet.



## Remarques
- Les URLs trouvées sont enregistrées dans le fichier `crawled_webpages.txt`.
- Les informations sur les pages web sont stockées dans la base de données SQLite `pages_web.db` qui est affiché à la fin de l'execution du main
- Chaque méthode de la classe Crawler est bien commentée sur le code


*Ce projet a été développé dans le cadre d'un TP sur l'indexation web.*
