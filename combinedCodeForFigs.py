"""
Combined script to create three figures showing PM2.5 data from different sources
during the June 2023 Canadian wildfire smoke event in Central New York
"""

import pandas as pd
import matplotlib.pyplot as plt

###########################################
# Figure 1: CDC MMWR Data (Meek et al.)
###########################################

# Data digitized from CDC MMWR
data = pd.DataFrame({
    'Date': range(1, 15),
    'Visits': [14, 15, 7, 7, 15, 23, 27, 15, 11, 10, 13, 15, 20, 15],
    'PM2.5': [10, 16, 10, 2, 22, 68, 110, 60, 20, 5, 10, 15, 15, 5],
    'PM2.5_Baseline': [5] * 14
})

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4), height_ratios=[1, 1.5])

# Top panel: ED visits
ax1.bar(data['Date'], data['Visits'], alpha=0.3, color='gray', label='Asthma ED Visits')
ax1.set_ylabel('No. of asthma ED visits', color='gray', fontsize=12)
ax1.tick_params(axis='y', labelcolor='gray')
ax1.set_ylim(0, 30)
ax1.grid(True, alpha=0.3)
ax1.legend()

# Bottom panel: PM2.5
ax2.plot(data['Date'], data['PM2.5'], 'b-', linewidth=2, label='PM2.5')
ax2.plot(data['Date'], data['PM2.5_Baseline'], 'b--', linewidth=1, label='PM2.5 Baseline')
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Daily mean PM₂.₅ (μg/m³)', color='b', fontsize=12)
ax2.tick_params(axis='y', labelcolor='b')
ax2.set_ylim(0, 120)
ax2.grid(True, alpha=0.3)
ax2.legend()

# Set identical x-axis limits for both plots
ax1.set_xlim(1, 14)
ax2.set_xlim(1, 14)

# Set x-ticks to show all dates
ax1.set_xticks(range(1, 15))
ax2.set_xticks(range(1, 15))

# Change x-tick labels to match the format of the other two figures
date_labels = pd.date_range(start='2023-06-01', end='2023-06-14').strftime('%Y-%m-%d')
ax1.set_xticklabels([date_labels[i-1] if i % 2 != 0 else '' for i in range(1, 15)], rotation=0)
ax2.set_xticklabels([date_labels[i-1] if i % 2 != 0 else '' for i in range(1, 15)], rotation=0)

# Set title for entire figure
fig.suptitle('Central region', fontsize=14, y=0.95)

# Adjust layout and save
plt.tight_layout()
plt.savefig('asthma_and_pm2p5_from_meek_et_al.png', dpi=300, bbox_inches='tight')
plt.close()

###########################################
# Figure 2: PurpleAir Data 
###########################################

# Read the files
ts_data = pd.read_csv('syracuse_ithaca_outdoor_pm25_june_2023.csv')
metadata = pd.read_csv('syracuse_ithaca_outdoor_pm25_june_2023_stats.csv')

# Convert Date to datetime
ts_data['Date'] = pd.to_datetime(ts_data['Date'])

# Shift dates by one full day to adjust for mismatch between GMT and Ithaca
ts_data['Date'] = ts_data['Date'] + pd.Timedelta(days=1)

# Create the plot
plt.figure(figsize=(15, 6))

# Plot data for each sensor
for sensor in ts_data['Sensor_Name'].unique():
    sensor_data = ts_data[ts_data['Sensor_Name'] == sensor]
    days_reported = metadata[metadata['Sensor_Name']==sensor]['Days_Reported'].values[0]
    plt.plot(sensor_data['Date'], 
             sensor_data['PM2.5'], 
             'o-',
             label=f"{sensor} (n={days_reported} days)",
             markersize=4)

plt.title('PM2.5 Measurements in Syracuse-Ithaca Region - June 2023', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('PM2.5 (µg/m³)', fontsize=12)
plt.ylim(0, 300)
plt.xlim(pd.Timestamp('2023-06-01'), pd.Timestamp('2023-06-14'))  # Set x-axis limits
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize=8)  # Move legend inside

# Adjust layout and save
plt.tight_layout()
plt.savefig('purple_air_data_from_central_region.png', dpi=300, bbox_inches='tight')
plt.close()

###########################################
# Figure 3: Air Quality Egg Data
###########################################

# List of file names
files = [
    'egg0004a30b00020a5a.csv',
    'egg0004a30b00020afd.csv',
    'egg0004a30b00026ea0.csv',
    'egg0004a30b0131c8a4.csv',
    'egg0004a30b0131e01b.csv',
    'egg0004a30b0131e02d.csv',
    'egg0004a30b0131e9b2.csv',
    'egg0004a30b0131fbb1.csv',
    'egg0004a30b000206b8.csv',
    'egg0004a30b000217c9.csv',
    'egg0004a30b000956f3.csv',
    'egg0004a30b01321af5.csv',
    'egg0004a30b013225e3.csv',
    'egg00802e8e050b0111.csv',
    'egg008043e602880141.csv',
    'egg008044e767090121.csv',
    'egg0080442c4cab0123.csv',
    'egg00804425ce180132.csv',
    'egg00804505d51b0120.csv',
    'egg0080435513280133.csv'
]

# Create empty list to store dataframes
dfs = []

# Read and combine all files
for file in files:
    try:
        df = pd.read_csv(f'./2023-CNY-Eggs/{file}')
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df = df.replace('---', pd.NA)
        df['pm2p5[ug/m^3]'] = pd.to_numeric(df['pm2p5[ug/m^3]'], errors='coerce')
        df['source'] = file.replace('.csv', '')
        if file == 'egg0080442c4cab0123.csv':
            df['source'] = 'Background'
        dfs.append(df)
        print(f"Successfully loaded: {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Combine all dataframes
if dfs:
    all_data = pd.concat(dfs, ignore_index=True)
    all_data = all_data.sort_values('timestamp')

    # Filter for June 1-14, 2023
    june_data = all_data[
        (all_data['timestamp'].dt.year == 2023) & 
        (all_data['timestamp'].dt.month == 6) &
        (all_data['timestamp'].dt.day >= 1) &
        (all_data['timestamp'].dt.day <= 14)
    ]

    # Create the plot
    plt.figure(figsize=(15, 6))

    # Plot pm2.5 data from each source
    for source in june_data['source'].unique():
        source_data = june_data[june_data['source'] == source]
        if source_data['pm2p5[ug/m^3]'].notna().any():
            plt.plot(source_data['timestamp'], 
                     source_data['pm2p5[ug/m^3]'], 
                     'o',markersize=2,  # Use dots instead of lines
                     label=source)

    plt.title('PM2.5 Measurements by Sensor - June 1-14, 2023', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('PM2.5 (μg/m³)', fontsize=12)
    plt.ylim(0, 350)
    plt.xlim(pd.Timestamp('2023-06-01'), pd.Timestamp('2023-06-14'))  # Set x-axis limits
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right', fontsize=8)  # Move legend inside

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('air_quality_eggs_from_central_region.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("No data was successfully loaded.")