import pandas as pd
import numpy as np
import glob
import os

# file_num = 1
# csv_files = glob.glob('../data/raw/*.csv') 

def clean_and_aggregate_data():
    raw_files = glob.glob('../data/raw/uwb_dataset_part*.csv')
    raw_data = pd.concat([pd.read_csv(f) for f in raw_files], ignore_index=True)
    print(f"Aggregated {len(raw_files)} raw files. Initial shape: {raw_data.shape}")

    # Step 2: Clean Data
    data_clean = raw_data.drop(columns=['CH', 'FRAME_LEN', 'BITRATE', 'PRFR', 'PREAM_LEN'])
    
    cir_columns = [f'CIR{i}' for i in range(1016)]
    data_clean['CIR_MEAN'] = data_clean[cir_columns].mean(axis=1)
    data_clean['CIR_VAR'] = data_clean[cir_columns].var(axis=1)
    data_clean['CIR_SKEW'] = data_clean[cir_columns].skew(axis=1)
    data_clean['CIR_ENERGY_FIRST_100'] = data_clean[cir_columns[:100]].sum(axis=1)

    # Step 3: Outlier Detection (Corrected)
    features_for_outliers = [
        'FP_IDX', 'FP_AMP1', 'FP_AMP2', 'FP_AMP3',
        'STDEV_NOISE', 'CIR_PWR', 'MAX_NOISE', 'RXPACC',
        'CIR_MEAN', 'CIR_VAR', 'CIR_SKEW', 'CIR_ENERGY_FIRST_100'
    ]

    Q1 = data_clean[features_for_outliers].quantile(0.25)
    Q3 = data_clean[features_for_outliers].quantile(0.75)
    IQR = Q3 - Q1
    
    # Corrected line with proper parentheses
    outliers = ((data_clean[features_for_outliers] < (Q1 - 1.5 * IQR)) | 
                (data_clean[features_for_outliers] > (Q3 + 1.5 * IQR)))
    
    outliers_mask = outliers.sum(axis=1) >= 3
    data_clean = data_clean[~outliers_mask]
    print(f"Data shape after outlier removal: {data_clean.shape}")

    # Step 4: Remove Duplicates
    data_clean = data_clean.drop_duplicates()
    print(f"Final cleaned shape: {data_clean.shape}")

    # Step 5: Save Aggregated Dataset
    processed_path = '../data/processed/aggregated_dataset.csv'
    data_clean.to_csv(processed_path, index=False)
    print(f"Saved aggregated dataset to {processed_path}")

if __name__ == '__main__':
    clean_and_aggregate_data()

# for file in csv_files:
#     csv_file = pd.read_csv(file)

#     # remove features that have little to zero correlation to the labels
#     data_w_dropped_cols = csv_file.drop(columns=['CH', 'FRAME_LEN', 'BITRATE', 'PRFR', 'PREAM_LEN'])
#     print(f'Successfully dropped unused columns in {csv_file}.')

#     # detect outliers
#     # extract summary statistics from CIR
#     data_w_dropped_cols['CIR_MEAN'] = data_w_dropped_cols.loc[:, 'CIR0':'CIR1015'].mean(axis=1)
#     data_w_dropped_cols['CIR_MAX'] = data_w_dropped_cols.loc[:, 'CIR0':'CIR1015'].max(axis=1)
#     data_w_dropped_cols['CIR_MIN'] = data_w_dropped_cols.loc[:, 'CIR0':'CIR1015'].min(axis=1)

#     # List of features for outlier detection
#     features_for_outliers = [
#         'FP_IDX',       
#         'FP_AMP1',      
#         'FP_AMP2',      
#         'FP_AMP3',      
#         'STDEV_NOISE',  
#         'CIR_PWR',      
#         'MAX_NOISE',    
#         'RXPACC',       
#         'CIR_MEAN',     
#         'CIR_MAX',      
#         'CIR_MIN'      
#     ]

#     # using iqr
#     Q1 = data_w_dropped_cols[features_for_outliers].quantile(0.25)
#     Q3 = data_w_dropped_cols[features_for_outliers].quantile(0.75)
#     IQR = Q3 - Q1
#     outliers_iqr = ((data_w_dropped_cols[features_for_outliers] < (Q1 - 1.5 * IQR)) | (data_w_dropped_cols[features_for_outliers] > (Q3 + 1.5 * IQR)))
#     print(f"Number of outliers detected using IQR: {outliers_iqr.sum()}")

#     # flag a row as an outlier if at least 3 features have outliers
#     outliers_multiple_features = outliers_iqr.sum(axis=1) >= 3  # adjust threshold as needed
#     print(f"Number of rows flagged as outliers: {outliers_multiple_features.sum()}")

#     # remove outliers
#     data_no_outliers = data_w_dropped_cols[~outliers_multiple_features]
#     print(f"Number of rows after removing outliers: {len(data_no_outliers)}")

#     # detect duplicates
#     duplicates = data_no_outliers.duplicated()
#     print(f"Number of duplicate rows detected: {duplicates.sum()}")

#     # remove duplicates (only if duplicates exist)
#     if duplicates.sum() > 0:
#         data_no_duplicates = data_no_outliers.drop_duplicates()
#         print(f"Number of rows after removing duplicates: {len(data_no_duplicates)}")
#     else:
#         data_no_duplicates = data_no_outliers  # no duplicates to remove
#         print("No duplicates found. Number of rows remains the same.")

#     # save cleaned data to new CSV file (after removing outliers and duplicates)
#     try:
#         # aggregated_data.to_csv(r'../data/cleaned/aggregated_dataset.csv', index=False) 
#         # print('Successfully aggregated datasets with dropped columns.')
#         data_no_outliers.to_csv(fr'../data/cleaned/cleaned_uwb_dataset_part{file_num}.csv', index=False)
#         print(f'Successfully uploaded cleaned data to cleaned_uwb_dataset_part{file_num} CSV file.')
#         file_num += 1
#     except:
#         print('Failed to upload cleaned data to new CSV file.')
#         file_num += 1
