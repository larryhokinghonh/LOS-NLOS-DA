import pandas as pd
import numpy as np
import glob

file_num = 1
csv_files = glob.glob('../data/raw/*.csv')

for file in csv_files:
    csv_file = pd.read_csv(file)

    # Remove features that have little to zero correlation to the labels
    data_w_dropped_cols = csv_file.drop(columns=['CH', 'FRAME_LEN', 'BITRATE', 'PRFR', 'PREAM_LEN'])
    print(f'Successfully dropped unused columns in {csv_file}.')

    # detect outliers
    # extract summary statistics from CIR
    data_w_dropped_cols['CIR_MEAN'] = data_w_dropped_cols.loc[:, 'CIR0':'CIR1015'].mean(axis=1)
    data_w_dropped_cols['CIR_MAX'] = data_w_dropped_cols.loc[:, 'CIR0':'CIR1015'].max(axis=1)
    data_w_dropped_cols['CIR_MIN'] = data_w_dropped_cols.loc[:, 'CIR0':'CIR1015'].min(axis=1)

    # List of features for outlier detection
    features_for_outliers = [
        'FP_IDX',       # First path index
        'FP_AMP1',      # First path amplitude part 1
        'FP_AMP2',      # First path amplitude part 2
        'FP_AMP3',      # First path amplitude part 3
        'STDEV_NOISE',  # Standard deviation of noise
        'CIR_PWR',      # Total channel impulse response power
        'MAX_NOISE',    # Maximum value of noise
        'RXPACC',       # Received RX preamble symbols
        'CIR_MEAN',     # Mean of CIR
        'CIR_MAX',      # Maximum of CIR
        'CIR_MIN'      # Minimum of CIR
    ]

    # using iqr
    Q1 = data_w_dropped_cols[features_for_outliers].quantile(0.25)
    Q3 = data_w_dropped_cols[features_for_outliers].quantile(0.75)
    IQR = Q3 - Q1
    outliers_iqr = ((data_w_dropped_cols[features_for_outliers] < (Q1 - 1.5 * IQR)) | (data_w_dropped_cols[features_for_outliers] > (Q3 + 1.5 * IQR)))
    print(f"Number of outliers detected using IQR: {outliers_iqr.sum()}")

    # flag a row as an outlier if at least 3 features have outliers
    outliers_multiple_features = outliers_iqr.sum(axis=1) >= 3  # adjust threshold as needed
    print(f"Number of rows flagged as outliers: {outliers_multiple_features.sum()}")

    # remove outliers
    data_no_outliers = data_w_dropped_cols[~outliers_multiple_features]
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
