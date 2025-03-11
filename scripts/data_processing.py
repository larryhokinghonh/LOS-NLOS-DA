import numpy as np
import pandas as pd

from google.cloud import storage
from google.oauth2 import service_account
import os, json, glob
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

def get_gcs_client():
    credentials_path = os.getenv('GCS_CREDENTIALS')
    if not credentials_path:
        raise ValueError('GCS_CREDENTIALS is empty')
    return storage.Client.from_service_account_json(credentials_path)

def upload_dataframe_to_gcs(df, bucket_name, destination_blob):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    # Convert DataFrame to CSV in-memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

    print(f"DataFrame uploaded to gs://{bucket_name}/{destination_blob}")

csv_files = glob.glob('../data/cleaned/*.csv')

aggregated_dataset = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=False)

upload_dataframe_to_gcs(aggregated_dataset, 'processed-los-nlos-data', 'aggregated_dataset.csv')

# Checking missing values in dataset
# dataset = aggregated_dataset.applymap(lambda x: not isinstance(x, (int, float))).sum()
# non_num_val_cols = dataset[dataset > 0].index.tolist()
# print('Columns with non-numeric values: ', non_num_val_cols)

# print('Number of missing values:')
# for col in cir_features.columns:
#     if cir_features[col].isna().sum() != 0:
#         print('\t%s: %d' % (col, cir_features[col].isna().sum()))

