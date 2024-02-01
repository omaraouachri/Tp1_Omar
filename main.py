from crawler import Crawler
import sqlite3


if __name__ == "__main__":
    # URL d'entrée
    start_url = "https://ensai.fr/"

    # Connexion à la base de données (créera la base de données si elle n'existe pas)

    conn = sqlite3.connect('pages_web.db')

        # Création d'un curseur pour exécuter des requêtes SQL
    cur = conn.cursor()

        # Création de la table pour stocker les pages web
        # Comme une page a un âge de 0 jusqu'à ce qu'elle soit modifiée, par défaut, on va assigner son age comme étant 0 une fois qu'on a crawlé

    cur.execute('''CREATE TABLE IF NOT EXISTS pages_web (
                        identifiant TEXT PRIMARY KEY,
                        url TEXT NOT NULL UNIQUE,
                        dernier_modif TEXT,
                        age INTEGER NOT NULL DEFAULT 0
                    )''')
    Crawler(url=start_url, max_per_page = 5, max_urls = 50).run()
    
    

        # Sélectionner toutes les colonnes de la table webpages
    cur.execute('SELECT * FROM pages_web')
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()


