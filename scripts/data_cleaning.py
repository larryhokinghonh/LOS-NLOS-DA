import pandas as pd
import numpy as np
from scipy.stats import zscore
import glob

file_num = 1
csv_files = glob.glob('../data/raw/*.csv')

for file in csv_files:
    csv_file = pd.read_csv(file)

    # Remove features that have little to zero correlation to the labels
    data_w_dropped_cols = csv_file.drop(columns=['CH', 'FRAME_LEN', 'BITRATE', 'PRFR'])
    print(f'Successfully dropped unused columns in {csv_file}.')

    # detect outliers
    # using IQR
    Q1 = data_w_dropped_cols.quantile(0.25)
    Q3 = data_w_dropped_cols.quantile(0.75)
    IQR = Q3 - Q1
    outliers_iqr = ((data_w_dropped_cols < (Q1 - 1.5 * IQR)) | (data_w_dropped_cols > (Q3 + 1.5 * IQR))).any(axis=1)
    print(f"Number of outliers detected using IQR: {outliers_iqr.sum()}")

    # remove outliers
    data_no_outliers = data_w_dropped_cols[~outliers_iqr]
    print(f"Number of rows after removing outliers: {len(data_no_outliers)}")

    # detect duplicates
    duplicates = data_no_outliers.duplicated()
    print(f"Number of duplicate rows detected: {duplicates.sum()}")

    # remove duplicates (only if duplicates exist)
    if duplicates.sum() > 0:
        data_no_duplicates = data_no_outliers.drop_duplicates()
        print(f"Number of rows after removing duplicates: {len(data_no_duplicates)}")
    else:
        data_no_duplicates = data_no_outliers  # no duplicates to remove
        print("No duplicates found. Number of rows remains the same.")

    # save cleaned data to new CSV file (after removing outliers and duplicates)
    try:
        # aggregated_data.to_csv(r'../data/cleaned/aggregated_dataset.csv', index=False) 
        # print('Successfully aggregated datasets with dropped columns.')
        data_no_outliers.to_csv(fr'../data/cleaned/cleaned_uwb_dataset_part{file_num}.csv', index=False)
        print(f'Successfully uploaded cleaned data to cleaned_uwb_dataset_part{file_num} CSV file.')
        file_num += 1
    except:
        print('Failed to upload cleaned data to new CSV file.')
        file_num += 1
