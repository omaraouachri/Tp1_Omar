import requests
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
from protego import Protego
import sqlite3
from datetime import datetime
import hashlib


    # Connexion à la base de données (créera la base de données si elle n'existe pas)

conn = sqlite3.connect('pages_web.db')

        # Création d'un curseur pour exécuter des requêtes SQL
cur = conn.cursor()





class Crawler:

    def __init__(self, url, max_per_page = 5, max_urls = 50):
        self.visited= []
        self.to_visit = [url]
        self.url = url
        self.max_per_page= max_per_page
        self.max_urls=max_urls



    
    def verifie_robots_txt(self, url_cible):
        '''
        Fonction qui vérifie si la page web est autorisée au crawler en utilisant robots.txt.
        
        Args:
            url_cible (str): L'URL de la page web à vérifier.

        Returns:
            bool: True si le crawling est autorisé, False sinon.
        '''
        # Obtient le contenu du fichier robots.txt
        response = requests.get(urljoin(self.url, "/robots.txt"))
        
        # Analyse le fichier robots.txt pour déterminer les règles d'autorisation
        parser_protego = Protego.parse(response.text)
        
        # Vérifie si le crawling est autorisé pour l'URL spécifiée
        autorise = parser_protego.can_fetch(url_cible, "*")

        # Affiche le résultat de la vérification
        if autorise:
            print(f"Le crawling de {url_cible} est autorisé.")
        else:
            print(f"Le crawling de {url_cible} n'est pas autorisé.")
        
        # Retourne le résultat
        return autorise
    


    

    def information_sitemap(self, url_sitemap) -> dict:
        """
        Cette méthode de classe récupère les URLs et leurs dates dans un sitemap.xml en utilisant le package requests pour le parsing.

        Args:
            - url_sitemap (str): L'URL du fichier sitemap.xml.

        Returns:
            - dict: Un dictionnaire contenant les URLs comme clés et leurs dates comme valeurs.
        """
        url_date = {}

        try:
            # Faire la requête HTTP pour récupérer le contenu du sitemap
            response = requests.get(url_sitemap, timeout=5)
            response.raise_for_status()  # Vérifier les erreurs HTTP

            # Parse le contenu XML
            root = ET.fromstring(response.content)

            # Itérer à travers les éléments du sitemap
            for child in root:
                # Vérifier si l'élément est un URL
                if child.tag.endswith('url'):
                    loc = child.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                    date = child.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text
                    url_date[loc] = date

            # Afficher le dictionnaire résultant
            print("Dictionnaire d'URLs et dates du sitemap:")
            for url, date in url_date.items():
                print(f"URL: {url}, Date: {date}")

            return url_date

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du sitemap à l'URL {url_sitemap}: {e}")
            return {}



    def crawl(self, url_cible: str):
        '''
        Cette fonction va crawler une page avec son URL,
        limiter le nombre de liens maximum à explorer par page,
        télécharger la page, et stocker le lien dans le fichier crawled_webpages.txt.
        '''

        # Créer un compteur i pour limiter le nombre de liens maximum à explorer par page
        i = 0

        # Télécharger la page
        response = requests.get(url_cible)

        # Vérifier si le téléchargement est réussi
        if response.status_code != 200:
            return  # Quitter si le téléchargement échoue

        html = response.text

        # Stocker le lien dans le fichier crawled_webpages.txt
        with open("crawled_webpages.txt", "a") as file:
            file.write(url_cible + "\n")

        # Parser la page html et chercher les liens
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            # Chercher tous les liens disponibles
            path = urljoin(url_cible, link.get('href', ''))

            # Vérifier si le nombre maximum a été atteint. Continuer jusqu'à max_urls_per_page.
            if i >= self.max_per_page:
                break

            # Vérifier si le lien est à visiter et s'il est autorisé par robots.txt
            if path not in self.visited and path not in self.to_visit and self.verifie_robots_txt(path):
                self.to_visit.append(path)
                i += 1
    
    

    def update_sqlite(self, url, dernier_modif):
        '''
            Cette fonction permet d'ajouter un nouvel élément à la base de données ou de mettre à jour un élément existant.
            Étant donné que les dates de dernière modification proviennent des sitemaps, certaines pages en dehors de ces sitemaps peuvent
            ne pas avoir de date de dernière modification associée. Dans de tels cas, cette fonction attribue un âge de 0 jours à ces pages.
        '''
        # Chaque document a pour identifiant unique un hash de l’URL
        url_hash = hashlib.sha256(url.encode()).hexdigest()

        # Vérifier si la page existe déjà dans la base de données
        cur.execute("SELECT * FROM pages_web WHERE url=?", (url,))
        existing_page = cur.fetchone()

        if dernier_modif is not None:
            age = (datetime.now() - datetime.strptime(dernier_modif, "%Y-%m-%dT%H:%M:%S+00:00")).days

        # Utilisation d'une seule condition pour déterminer si la page existe déjà
        if existing_page:
            # Mettre à jour l'âge de la page
            cur.execute("UPDATE pages_web SET dernier_modif=?, age=? WHERE url=?", (dernier_modif, age, url))
        else:
            # Ajouter la nouvelle page avec un âge initial de 0
            cur.execute("INSERT INTO pages_web (identifiant, url, dernier_modif) VALUES (?, ?, ?)", (url_hash, url, dernier_modif))

        conn.commit()
        




    

    def run(self):
        '''
            Cette fonction va lancer le crawler pour les tâches demandées dans le sujet
        '''
        # On crée un dictionnaire pour stocker les urls et dates trouvés dans les sitemap.xml
        url_date = {}
        if True:
            # Lire les fichiers sitemap.xml des sites pour réduire les requêtes aux urls
            r = requests.get(urljoin(self.url, "/robots.txt"))
            rp = Protego.parse(r.text)
            sitemaps = rp.sitemaps
            for sitemap in sitemaps:
                # dict_url est un dictionnaire pour stocker les urls et dates trouvés dans un sitemaps, puis on va l'ajouter dans la dictionnaire globale url_date plus tard
                dict_url  = self.information_sitemap(sitemap)
                for loc in dict_url.keys():
                    self.to_visit.append(loc)
                url_date.update(dict_url)

        # Boucle pour visiter tous les urls dans le urls_to_visit (frontier) si les conditions sont satisfaites
        while self.to_visit and len(self.visited) < self.max_urls:
            url = self.to_visit.pop(0)
            print(url)
            # Pour gérer des Exceptions qui peuvent être levé durant le processus de crawling et éviter l'arrêt inattendu de code, on va les mettre dans un try bloc
            try:
                self.crawl(url)
                # Une fois la page a été crawlée, on va l'ajouter ou la mettre à jours dans la base de donnée
                dernier_modif = url_date.get(url) 
                self.update_sqlite(url, dernier_modif)
        
            except Exception as e:
                print(f'Failed to crawl {url}: {str(e)}')
            finally:
                self.visited.append(url)
            # Respecter la politesse en attendant 5 secondes entre chaque appel
            sleep(5)
