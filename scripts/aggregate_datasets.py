import pandas as pd
import glob

cleaned_files = glob.glob('../data/cleaned/cleaned_uwb_dataset_part*.csv')

# Load all cleaned datasets into a list of DataFrames
dataframes = [pd.read_csv(file) for file in cleaned_files]

aggregated_data = pd.concat(dataframes, ignore_index=True)

# Save aggregated dataset
aggregated_data.to_csv('../data/processed/aggregated_dataset.csv', index=False)
print(f"Aggregated dataset saved with {len(aggregated_data)} rows.")