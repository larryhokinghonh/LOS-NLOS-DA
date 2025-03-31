import pandas as pd
from google.cloud import storage
import os, glob
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

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

    print(f"DataFrame uploaded to gs://{bucket_name}/{destination_blob}")

def clean_and_aggregate_data():
    raw_files = glob.glob('../data/raw/uwb_dataset_part*.csv')
    raw_data = pd.concat([pd.read_csv(f) for f in raw_files], ignore_index=True)
    print(f"Aggregated {len(raw_files)} raw files. Initial shape: {raw_data.shape}")

    data_clean = raw_data.drop(columns=['CH', 'FRAME_LEN', 'BITRATE', 'PRFR', 'PREAM_LEN'])
    
    cir_columns = [f'CIR{i}' for i in range(1016)]
    data_clean['CIR_MEAN'] = data_clean[cir_columns].mean(axis=1)
    data_clean['CIR_VAR'] = data_clean[cir_columns].var(axis=1)
    data_clean['CIR_SKEW'] = data_clean[cir_columns].skew(axis=1)
    data_clean['CIR_ENERGY_FIRST_100'] = data_clean[cir_columns[:100]].sum(axis=1)

    features_for_outliers = [
        'FP_IDX', 'FP_AMP1', 'FP_AMP2', 'FP_AMP3',
        'STDEV_NOISE', 'CIR_PWR', 'MAX_NOISE', 'RXPACC',
        'CIR_MEAN', 'CIR_VAR', 'CIR_SKEW', 'CIR_ENERGY_FIRST_100'
    ]

    Q1 = data_clean[features_for_outliers].quantile(0.25)
    Q3 = data_clean[features_for_outliers].quantile(0.75)
    IQR = Q3 - Q1
    
    outliers = ((data_clean[features_for_outliers] < (Q1 - 1.5 * IQR)) | 
                (data_clean[features_for_outliers] > (Q3 + 1.5 * IQR)))
    
    outliers_mask = outliers.sum(axis=1) >= 3
    data_clean = data_clean[~outliers_mask]
    print(f"Data shape after outlier removal: {data_clean.shape}")

    data_clean = data_clean.drop_duplicates()
    print(f"Final cleaned shape: {data_clean.shape}")

    processed_path = '../data/processed/aggregated_dataset.csv'
    data_clean.to_csv(processed_path, index=False)
    print(f"Saved aggregated dataset to {processed_path}")

    upload_dataframe_to_gcs(data_clean, 'processed-los-nlos-data', 'aggregated_dataset.csv')

if __name__ == '__main__':
    clean_and_aggregate_data()
