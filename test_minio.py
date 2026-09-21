import boto3
from botocore.client import Config

# Connexion à MinIO
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin123',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# Lister les buckets
buckets = s3.list_buckets()
print("Buckets MinIO:", [b['Name'] for b in buckets['Buckets']])

# Créer un bucket si nécessaire
s3.create_bucket(Bucket='emploi-data')
print("✅ Bucket 'emploi-data' créé")