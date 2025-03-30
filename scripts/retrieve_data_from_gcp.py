from google.cloud import storage
from dotenv import load_dotenv
import os

load_dotenv()

def get_gcs_client():
    credentials_path = os.getenv('GCS_CREDENTIALS')
    if not credentials_path:
        raise ValueError('GCS_CREDENTIALS is empty')
    return storage.Client.from_service_account_json(credentials_path)

def download_from_gcs(bucket_name, source_blob, destination_file):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob)
    blob.download_to_filename(destination_file)
    print(f'File {source_blob} downloaded to {destination_file}')

download_from_gcs('processed-los-nlos-data', 'aggregated_dataset.csv', '../data/processed/aggregated_dataset.csv')