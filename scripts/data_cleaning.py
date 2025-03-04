import pandas as pd
import glob

file_num = 1
csv_files = glob.glob('../data/raw/*.csv')

for file in csv_files:
    csv_file = pd.read_csv(file)

    # Remove features that have little to zero correlation to the labels
    data_w_dropped_cols = csv_file.drop(columns=['CH', 'FRAME_LEN', 'BITRATE', 'PRFR'])
    print(f'Successfully dropped unused columns in {csv_file}.')

    try:
        # aggregated_data.to_csv(r'../data/cleaned/aggregated_dataset.csv', index=False) 
        # print('Successfully aggregated datasets with dropped columns.')
        data_w_dropped_cols.to_csv(fr'../data/cleaned/cleaned_uwb_dataset_part{file_num}.csv', index=False)
        print(f'Successfully uploaded cleaned data to cleaned_uwb_dataset_part{file_num} CSV file.')
        file_num += 1
    except:
        print('Failed to upload cleaned data to new CSV file.')
        file_num += 1

# detect outliers

# detect duplicates