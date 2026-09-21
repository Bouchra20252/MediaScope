from minio import Minio
import os
import glob

# Connexion à MinIO (port 9005 au lieu de 9000)
client = Minio(
    "localhost:9005",        # ← Changé : 9000 → 9005
    access_key="minioadmin",
    secret_key="minioadmin123",
    secure=False
)

# Créer les buckets s'ils n'existent pas
buckets = ["bronze-articles", "silver-articles", "gold-articles"]
for bucket in buckets:
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"✅ Bucket '{bucket}' créé")
    else:
        print(f"ℹ️ Bucket '{bucket}' existe déjà")

# Upload des fichiers bronze
bronze_files = glob.glob("data/bronze/*.json")
print(f"\n📁 Upload des fichiers bronze ({len(bronze_files)} fichiers):")
for f in bronze_files:
    filename = os.path.basename(f)
    client.fput_object("bronze-articles", filename, f)
    print(f"   ✅ {filename}")

# Upload des fichiers silver
silver_files = glob.glob("data/silver/*.parquet")
print(f"\n📁 Upload des fichiers silver ({len(silver_files)} fichiers):")
for f in silver_files:
    filename = os.path.basename(f)
    client.fput_object("silver-articles", filename, f)
    print(f"   ✅ {filename}")

print("\n🎉 Tous les fichiers ont été uploadés dans MinIO !")