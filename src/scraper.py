"""
Scraper MédiaScope - Version avec données mockées complètes
40 articles (10 par source : CNN, Al Jazeera, BBC, Reuters)
"""

import json
import os
import time
from datetime import datetime
import pandas as pd

# =====================================================
# DONNÉES MOCKÉES COMPLÈTES (40 ARTICLES)
# =====================================================

ARTICLES_COMPLETS = []

# CNN (10 articles)
cnn_articles = [
    {"titre": "Breaking: US election results 2024 live updates", "auteur": "CNN Staff", "date_publication": "2024-01-15", "categorie": "Politique", "contenu": "Les résultats des élections américaines 2024 sont en cours de dépouillement...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/15/politics/us-election-results/index.html"},
    {"titre": "Israel-Hamas war: Ceasefire negotiations continue", "auteur": "CNN Staff", "date_publication": "2024-01-16", "categorie": "International", "contenu": "Les négociations de cessez-le-feu se poursuivent au Qatar...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/16/middleeast/israel-hamas-ceasefire/index.html"},
    {"titre": "Climate crisis: Record temperatures across Europe", "auteur": "CNN Staff", "date_publication": "2024-01-17", "categorie": "Environnement", "contenu": "L'Europe connaît des températures record...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/17/europe/climate-record-temperatures/index.html"},
    {"titre": "Apple unveils new AI features at WWDC 2024", "auteur": "CNN Staff", "date_publication": "2024-01-18", "categorie": "Technologie", "contenu": "Apple a dévoilé ses nouvelles fonctionnalités d'IA...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/18/tech/apple-ai-features/index.html"},
    {"titre": "Stock market: Dow Jones hits record high", "auteur": "CNN Staff", "date_publication": "2024-01-19", "categorie": "Économie", "contenu": "Le Dow Jones a atteint un nouveau record...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/19/investing/dow-jones-record/index.html"},
    {"titre": "NASA announces new Mars mission for 2026", "auteur": "CNN Staff", "date_publication": "2024-01-20", "categorie": "Science", "contenu": "La NASA prépare une nouvelle mission vers Mars...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/20/tech/nasa-mars-mission/index.html"},
    {"titre": "Football: Champions League quarter-finals preview", "auteur": "CNN Staff", "date_publication": "2024-01-21", "categorie": "Sport", "contenu": "Les quarts de finale de la Ligue des Champions approchent...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/21/sport/champions-league-preview/index.html"},
    {"titre": "Health alert: New COVID variant detected", "auteur": "CNN Staff", "date_publication": "2024-01-22", "categorie": "Santé", "contenu": "Un nouveau variant du COVID-19 a été détecté...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/22/health/new-covid-variant/index.html"},
    {"titre": "Cyber attack: Major companies hit by ransomware", "auteur": "CNN Staff", "date_publication": "2024-01-23", "categorie": "Technologie", "contenu": "Plusieurs grandes entreprises victimes d'une cyberattaque...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/23/tech/ransomware-cyber-attack/index.html"},
    {"titre": "Hollywood strikes end after historic agreement", "auteur": "CNN Staff", "date_publication": "2024-01-24", "categorie": "Divertissement", "contenu": "Les grèves à Hollywood prennent fin...", "source": "CNN", "url": "https://edition.cnn.com/2024/01/24/entertainment/hollywood-strike-ends/index.html"}
]

# Al Jazeera (10 articles)
aj_articles = [
    {"titre": "Gaza: Humanitarian crisis worsens as aid blocked", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-15", "categorie": "International", "contenu": "La crise humanitaire à Gaza s'aggrave...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/15/gaza-humanitarian-crisis-worsens"},
    {"titre": "Saudi Arabia hosts Arab League summit on Gaza", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-16", "categorie": "Politique", "contenu": "L'Arabie Saoudite accueille un sommet de la Ligue arabe...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/16/saudi-arabia-hosts-arab-league-summit"},
    {"titre": "Africa's new trade agreement boosts continental economy", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-17", "categorie": "Économie", "contenu": "Le nouvel accord commercial africain stimule l'économie...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/economy/2024/1/17/africa-trade-agreement"},
    {"titre": "Climate change: Sahara desert experiences rare floods", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-18", "categorie": "Environnement", "contenu": "Le désert du Sahara connaît des inondations historiques...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/18/sahara-desert-floods"},
    {"titre": "Qatar launches national AI strategy for 2030", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-19", "categorie": "Technologie", "contenu": "Le Qatar lance sa stratégie nationale en IA...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/19/qatar-national-ai-strategy"},
    {"titre": "World Cup 2030: Morocco prepares for historic event", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-20", "categorie": "Sport", "contenu": "Le Maroc se prépare à accueillir la Coupe du Monde 2030...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/sports/2024/1/20/morocco-world-cup-2030"},
    {"titre": "OPEC+ announces surprise oil production cuts", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-21", "categorie": "Économie", "contenu": "L'OPEC+ annonce des réductions surprises de la production...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/economy/2024/1/21/opec-oil-production-cuts"},
    {"titre": "Egypt opens new Suez Canal expansion", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-22", "categorie": "Économie", "contenu": "L'Égypte inaugure une nouvelle expansion du Canal de Suez...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/22/egypt-suez-canal-expansion"},
    {"titre": "Turkey-Syria earthquake: One year later", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-23", "categorie": "International", "contenu": "Un an après le séisme dévastateur en Turquie et Syrie...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/23/turkey-syria-earthquake-anniversary"},
    {"titre": "UAE launches first Arab mission to asteroid belt", "auteur": "Al Jazeera Staff", "date_publication": "2024-01-24", "categorie": "Science", "contenu": "Les EAU lancent la première mission arabe vers la ceinture d'astéroïdes...", "source": "Al Jazeera", "url": "https://www.aljazeera.com/news/2024/1/24/uae-asteroid-mission"}
]

# BBC News (10 articles)
bbc_articles = [
    {"titre": "UK general election: Polls show tight race", "auteur": "BBC Staff", "date_publication": "2024-01-15", "categorie": "Politique", "contenu": "Les sondages montrent une course serrée...", "source": "BBC News", "url": "https://www.bbc.com/news/uk-politics-67987654"},
    {"titre": "Farmers protests continue across France and Germany", "auteur": "BBC Staff", "date_publication": "2024-01-16", "categorie": "Société", "contenu": "Les manifestations d'agriculteurs se poursuivent...", "source": "BBC News", "url": "https://www.bbc.com/news/world-europe-67987655"},
    {"titre": "King Charles returns to public duties", "auteur": "BBC Staff", "date_publication": "2024-01-17", "categorie": "People", "contenu": "Le roi Charles reprend ses fonctions publiques...", "source": "BBC News", "url": "https://www.bbc.com/news/uk-67987656"},
    {"titre": "Bank of England holds interest rates at 5.25%", "auteur": "BBC Staff", "date_publication": "2024-01-18", "categorie": "Économie", "contenu": "La Banque d'Angleterre maintient ses taux...", "source": "BBC News", "url": "https://www.bbc.com/news/business-67987657"},
    {"titre": "Scotland aims for net zero emissions by 2045", "auteur": "BBC Staff", "date_publication": "2024-01-19", "categorie": "Environnement", "contenu": "L'Écosse vise la neutralité carbone...", "source": "BBC News", "url": "https://www.bbc.com/news/science-environment-67987658"},
    {"titre": "Wimbledon 2024: Preview and top seeds announced", "auteur": "BBC Staff", "date_publication": "2024-01-20", "categorie": "Sport", "contenu": "Le tournoi de Wimbledon 2024 approche...", "source": "BBC News", "url": "https://www.bbc.com/sport/tennis-67987659"},
    {"titre": "NHS faces winter crisis as cases rise", "auteur": "BBC Staff", "date_publication": "2024-01-21", "categorie": "Santé", "contenu": "Le NHS fait face à une crise hivernale...", "source": "BBC News", "url": "https://www.bbc.com/news/health-67987660"},
    {"titre": "Oxford University develops new cancer treatment", "auteur": "BBC Staff", "date_publication": "2024-01-22", "categorie": "Science", "contenu": "L'Université d'Oxford développe un nouveau traitement...", "source": "BBC News", "url": "https://www.bbc.com/news/health-67987661"},
    {"titre": "British Museum returns artifacts to Greece", "auteur": "BBC Staff", "date_publication": "2024-01-23", "categorie": "Culture", "contenu": "Le British Museum annonce le retour d'artefacts...", "source": "BBC News", "url": "https://www.bbc.com/news/entertainment-arts-67987662"},
    {"titre": "London becomes world's first National Park City", "auteur": "BBC Staff", "date_publication": "2024-01-24", "categorie": "Environnement", "contenu": "Londres devient la première ville parc national...", "source": "BBC News", "url": "https://www.bbc.com/news/uk-england-london-67987663"}
]

# Reuters (10 articles)
reuters_articles = [
    {"titre": "Global markets rally after Fed signals rate cuts", "auteur": "Reuters Staff", "date_publication": "2024-01-15", "categorie": "Économie", "contenu": "Les marchés mondiaux grimpent...", "source": "Reuters", "url": "https://www.reuters.com/markets/global-markets-fed-rate-cuts-2024-01-15/"},
    {"titre": "Oil prices drop as OPEC+ increases production", "auteur": "Reuters Staff", "date_publication": "2024-01-16", "categorie": "Économie", "contenu": "Les prix du pétrole chutent...", "source": "Reuters", "url": "https://www.reuters.com/business/energy/oil-prices-opec-production-2024-01-16/"},
    {"titre": "Apple surpasses Microsoft as world's most valuable company", "auteur": "Reuters Staff", "date_publication": "2024-01-17", "categorie": "Technologie", "contenu": "Apple dépasse Microsoft...", "source": "Reuters", "url": "https://www.reuters.com/technology/apple-most-valuable-company-2024-01-17/"},
    {"titre": "Bitcoin hits new all-time high above $75,000", "auteur": "Reuters Staff", "date_publication": "2024-01-18", "categorie": "Finance", "contenu": "Le Bitcoin atteint un nouveau record...", "source": "Reuters", "url": "https://www.reuters.com/markets/currencies/bitcoin-all-time-high-2024-01-18/"},
    {"titre": "Tesla recalls 2 million vehicles over safety concerns", "auteur": "Reuters Staff", "date_publication": "2024-01-19", "categorie": "Automobile", "contenu": "Tesla rappelle 2 millions de véhicules...", "source": "Reuters", "url": "https://www.reuters.com/business/autos-transportation/tesla-recall-2-million-vehicles-2024-01-19/"},
    {"titre": "China's economy shows signs of recovery", "auteur": "Reuters Staff", "date_publication": "2024-01-20", "categorie": "Économie", "contenu": "L'économie chinoise montre des signes de reprise...", "source": "Reuters", "url": "https://www.reuters.com/markets/china-economy-recovery-2024-01-20/"},
    {"titre": "War in Ukraine: Russia launches new offensive", "auteur": "Reuters Staff", "date_publication": "2024-01-21", "categorie": "International", "contenu": "La Russie lance une nouvelle offensive...", "source": "Reuters", "url": "https://www.reuters.com/world/europe/ukraine-war-russia-offensive-2024-01-21/"},
    {"titre": "Goldman Sachs reports record quarterly profits", "auteur": "Reuters Staff", "date_publication": "2024-01-22", "categorie": "Finance", "contenu": "Goldman Sachs annonce des bénéfices records...", "source": "Reuters", "url": "https://www.reuters.com/business/finance/goldman-sachs-record-profits-2024-01-22/"},
    {"titre": "Boeing faces new delays in 737 Max deliveries", "auteur": "Reuters Staff", "date_publication": "2024-01-23", "categorie": "Industrie", "contenu": "Boeing fait face à de nouveaux retards...", "source": "Reuters", "url": "https://www.reuters.com/business/aerospace-defense/boeing-737-max-delays-2024-01-23/"},
    {"titre": "EU announces new sanctions against Russia", "auteur": "Reuters Staff", "date_publication": "2024-01-24", "categorie": "Politique", "contenu": "L'UE annonce de nouvelles sanctions contre la Russie...", "source": "Reuters", "url": "https://www.reuters.com/world/europe/eu-sanctions-russia-2024-01-24/"}
]

# Assemblage des 40 articles
ARTICLES_COMPLETS = cnn_articles + aj_articles + bbc_articles + reuters_articles

def scrape_tous_sites():
    """Récupère tous les articles (version mockée complète)"""
    print("🕷️ DÉBUT DU SCRAPING DES ACTUALITÉS")
    print("=" * 50)
    print("Sources: CNN, Al Jazeera, BBC News, Reuters")
    print("=" * 50)
    
    articles = ARTICLES_COMPLETS.copy()
    
    print(f"  ✅ CNN: 10 articles")
    print(f"  ✅ Al Jazeera: 10 articles")
    print(f"  ✅ BBC News: 10 articles")
    print(f"  ✅ Reuters: 10 articles")
    print("=" * 50)
    print(f"✅ TOTAL GÉNÉRAL: {len(articles)} articles")
    
    return articles

def sauvegarder_bronze(articles, output_dir="data/bronze"):
    """Sauvegarde les articles bruts en JSON"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/articles_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Articles sauvegardés dans: {filename}")
    return filename

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 EXÉCUTION DU SCRAPER MÉDIASCOPE")
    print("=" * 50)
    
    articles = scrape_tous_sites()
    sauvegarder_bronze(articles)
    
    df = pd.DataFrame(articles)
    print("\n📊 STATISTIQUES PAR SOURCE:")
    stats = df['source'].value_counts()
    for source, count in stats.items():
        print(f"  - {source}: {count} articles")
    
    print("\n" + "=" * 50)
    print("✅ Scraper terminé avec succès!")
    print("=" * 50)