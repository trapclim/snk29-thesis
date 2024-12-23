import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def read_traj_file(filename):
    """
    Read trajectory file and return a dictionary where:
    - keys are trajectory numbers (1 to n)
    - values are dictionaries containing 'lats' and 'lons' arrays
    """
    trajectories = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    # Skip header lines
    data_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('1 PRESSURE'):
            data_start = i + 1
            break
    
    # Read trajectory data
    for line in lines[data_start:]:
        parts = line.strip().split()
        if len(parts) >= 10:  # Ensure line has enough elements
            traj_num = int(parts[0])
            lat = float(parts[9])
            lon = float(parts[10])
            
            if traj_num not in trajectories:
                trajectories[traj_num] = {'lats': [], 'lons': []}
            
            trajectories[traj_num]['lats'].append(lat)
            trajectories[traj_num]['lons'].append(lon)
    
    # Convert lists to numpy arrays for better handling
    for traj in trajectories.values():
        traj['lats'] = np.array(traj['lats'])
        traj['lons'] = np.array(traj['lons'])
            
    return trajectories

# Read the fire CSV file
df = pd.read_csv('NFDB_filtered_point_20240613.txt', delimiter=',',encoding='latin1')

# Read both trajectory files
trajectories1 = read_traj_file('tdump.138766.txt')  # Replace with your first file name
trajectories2 = read_traj_file('tdump.138880.txt')  # Replace with your second file name

# Convert the REP_DATE to datetime
df['REP_DATE'] = pd.to_datetime(df['REP_DATE'])

# Create masks for filtering
date_mask = (df['REP_DATE'] >= '2023-06-01') & (df['REP_DATE'] <= '2023-06-07')
lat_mask = (df['LATITUDE'] >= 46) & (df['LATITUDE'] <= 52)
lon_mask = (df['LONGITUDE'] >= -80) & (df['LONGITUDE'] <= -70)

# Apply all filters
filtered_df = df[date_mask & lat_mask & lon_mask]

# Create the map
plt.figure(figsize=(8, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set map extent [lon_min, lon_max, lat_min, lat_max]
ax.set_extent([-90, -63, 36, 53], crs=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.LAKES, alpha=0.5)

# Add gridlines
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Plot first set of trajectories
for traj_num, traj_data in trajectories1.items():
    ax.plot(traj_data['lons'], 
            traj_data['lats'],
            color='orange',
            transform=ccrs.PlateCarree(),
            zorder=1,
            label='Ithaca Back Trajectories' if traj_num == 1 else "")

# Plot second set of trajectories
for traj_num, traj_data in trajectories2.items():
    ax.plot(traj_data['lons'], 
            traj_data['lats'],
            color='coral',  # Similar but different color
            transform=ccrs.PlateCarree(),
            zorder=1,
            label='Syracuse Back Trajectories' if traj_num == 1 else "")

# Plot the fire points
if len(filtered_df) > 0:
    plt.scatter(filtered_df['LONGITUDE'], 
               filtered_df['LATITUDE'],
               color='red',
               transform=ccrs.PlateCarree(),
               label='Fire locations',
               zorder=2)
    
    # Print the coordinates
    print("Filtered coordinates:")
    print(filtered_df[['LATITUDE', 'LONGITUDE', 'REP_DATE']])
else:
    print("No points found matching the criteria")

# Add title and legend
plt.title('Fire Locations (June 1-7, 2023) with Back Trajectories')
plt.legend()

# Show and save the plot
plt.savefig('fire_locations_map.png', dpi=300, bbox_inches='tight')

plt.show()