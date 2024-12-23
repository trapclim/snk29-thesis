import pandas as pd
import matplotlib.pyplot as plt


###########################################
# Figure 4: Air Quality Egg PM10 and PM1 Data
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
        df['pm10p0[ug/m^3]'] = pd.to_numeric(df['pm10p0[ug/m^3]'], errors='coerce')
        df['pm1p0[ug/m^3]'] = pd.to_numeric(df['pm1p0[ug/m^3]'], errors='coerce')
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

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

    # Top panel: PM10
    for source in june_data['source'].unique():
        source_data = june_data[june_data['source'] == source]
        if source_data['pm10p0[ug/m^3]'].notna().any():
            ax1.plot(source_data['timestamp'], 
                    source_data['pm10p0[ug/m^3]'], 
                    'o',
                    label=source)
    
    ax1.set_ylabel('PM10 (μg/m³)', fontsize=12)
    ax1.set_ylim(0, 350)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_xlim(pd.Timestamp('2023-06-06'), pd.Timestamp('2023-06-09'))  # Set x-axis limits

    # Bottom panel: PM1
    for source in june_data['source'].unique():
        source_data = june_data[june_data['source'] == source]
        if source_data['pm1p0[ug/m^3]'].notna().any():
            ax2.plot(source_data['timestamp'], 
                    source_data['pm1p0[ug/m^3]'], 
                    'o',
                    label=source)

    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('PM1 (μg/m³)', fontsize=12)
    ax2.set_ylim(0, 350)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper right', fontsize=8)
    ax2.set_xlim(pd.Timestamp('2023-06-06'), pd.Timestamp('2023-06-11'))  # Set x-axis limits

    # Set title for entire figure
    fig.suptitle('PM10 and PM1 Measurements by Sensor - June 6-11, 2023', fontsize=14)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('air_quality_eggs_pm10_pm1_from_central_region.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print("No data was successfully loaded.")