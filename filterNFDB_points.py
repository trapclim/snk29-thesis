import pandas as pd

# Read the fire CSV file
df = pd.read_csv('NFDB_point_20240613.txt', delimiter=',', encoding='latin1')

# Convert the REP_DATE to datetime
df['REP_DATE'] = pd.to_datetime(df['REP_DATE'])

# Create masks for filtering
date_mask = (df['REP_DATE'] >= '2023-06-01') & (df['REP_DATE'] <= '2023-06-07')
lat_mask = (df['LATITUDE'] >= 46) & (df['LATITUDE'] <= 52)
lon_mask = (df['LONGITUDE'] >= -80) & (df['LONGITUDE'] <= -70)

# Apply all filters
filtered_df = df[date_mask & lat_mask & lon_mask]

# Save the filtered dataframe to a new file
# Using the same format as the original file
filtered_df.to_csv('NFDB_filtered_point_20240613.txt', index=False)