import pandas as pd
import json
import os
from datetime import datetime

print("=" * 50)
print("🧹 CLEANER MÉDIASCOPE - VERSION CORRIGÉE")
print("=" * 50)

# Lister les fichiers bronze
bronze_files = [f for f in os.listdir("data/bronze") if f.startswith("articles_") and f.endswith(".json")]

if not bronze_files:
    print("❌ Aucun fichier articles_.json trouvé dans data/bronze/")
    print("   Fichiers présents:", os.listdir("data/bronze"))
    exit()

print(f"📂 Fichiers bronze disponibles:")
for f in bronze_files:
    print(f"   - {f}")

# Prendre le plus récent
latest = max(bronze_files)
print(f"\n✅ Chargement: {latest}")

with open(f"data/bronze/{latest}", "r", encoding="utf-8") as f:
    articles = json.load(f)

df = pd.DataFrame(articles)
print(f"\n📊 {len(df)} articles chargés")

# Vérifier les sources
print("\n📰 SOURCES dans le fichier bronze:")
for source, count in df['source'].value_counts().items():
    print(f"   {source}: {count}")

# Fonction de catégorisation simple
def get_categorie(titre):
    t = str(titre).lower()
    if 'election' in t or 'president' in t or 'politique' in t: return 'Politique'
    if 'economie' in t or 'marche' in t or 'finance' in t: return 'Économie'
    if 'technologie' in t or 'ia' in t or 'apple' in t: return 'Technologie'
    if 'sport' in t or 'football' in t or 'champions' in t: return 'Sport'
    if 'sante' in t or 'covid' in t or 'health' in t: return 'Santé'
    if 'climat' in t or 'environnement' in t: return 'Environnement'
    if 'gaza' in t or 'israel' in t or 'ukraine' in t: return 'International'
    return 'Divers'

df['categorie_detectee'] = df['titre'].apply(get_categorie)
df['longueur_titre'] = df['titre'].str.len()
df['qualite_score'] = 100
df['est_valide'] = True
df['date_traitement'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Sauvegarde
os.makedirs("data/silver", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output = f"data/silver/articles_nettoyes_{timestamp}.parquet"
df.to_parquet(output, index=False)

print(f"\n💾 Sauvegardé: {output}")
print(f"\n📊 STATISTIQUES FINALES:")
for source, count in df['source'].value_counts().items():
    print(f"   {source}: {count}")

print("\n✅ CLEANER TERMINÉ!")