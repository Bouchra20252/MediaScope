"""
DAG Airflow pour MédiaScope
Planifie l'exécution quotidienne du scraper et du cleaner
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

# Configuration par défaut
default_args = {
    'owner': 'mediascope',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définition du DAG
with DAG(
    'mediascope_pipeline',
    default_args=default_args,
    description='Pipeline MédiaScope : Scraping + Nettoyage',
    schedule_interval='0 */6 * * *',  # Toutes les 6 heures
    catchup=False,
    tags=['mediascope', 'etl'],
) as dag:

    # Tâche de début
    start = DummyOperator(task_id='start')

    # Tâche 1 : Scraper les articles
    scrape_task = BashOperator(
        task_id='scrape_articles',
        bash_command='cd C:/Users/idris/Documents/arcitecture\ des\ donnee/projet\ mediascope2 && python src/scraper.py',
    )

    # Tâche 2 : Nettoyer les données
    clean_task = BashOperator(
        task_id='clean_articles',
        bash_command='cd C:/Users/idris/Documents/arcitecture\ des\ donnee/projet\ mediascope2 && python src/cleaner.py',
    )

    # Tâche de fin
    end = DummyOperator(task_id='end')

    # Définition de l'ordre d'exécution
    start >> scrape_task >> clean_task >> end