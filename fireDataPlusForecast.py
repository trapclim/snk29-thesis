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
            lat = float(parts[9])  # Changed from parts[8]
            lon = float(parts[10])  # Changed from parts[9]
            
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

# Read trajectories
trajectories = read_traj_file('tdump.154659.txt')

# Convert the REP_DATE to datetime
df['REP_DATE'] = pd.to_datetime(df['REP_DATE'])

# Create masks for filtering
date_mask = (df['REP_DATE'] >= '2023-06-01') & (df['REP_DATE'] <= '2023-06-07')
lat_mask = (df['LATITUDE'] >= 46) & (df['LATITUDE'] <= 55)
lon_mask = (df['LONGITUDE'] >= -80) & (df['LONGITUDE'] <= -70)

# Apply all filters
filtered_df = df[date_mask & lat_mask & lon_mask]

# Filter for the 5 northernmost fire points between 75W and 70W
northernmost_fires = filtered_df[(filtered_df['LONGITUDE'] >= -80) & (filtered_df['LONGITUDE'] <= -75)]
northernmost_fires = northernmost_fires.nlargest(7, 'LATITUDE')

# Print the coordinates of the 5 northernmost fire points
print("5 Northernmost fire points between 75W and 70W:")
print(northernmost_fires[['LATITUDE', 'LONGITUDE']])

# Create the map
plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set map extent [lon_min, lon_max, lat_min, lat_max]
ax.set_extent([-90, -63, 36, 58], crs=ccrs.PlateCarree())

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.STATES)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.LAKES, alpha=0.5)

# Add gridlines
gl = ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Plot each trajectory independently
for traj_num, traj_data in trajectories.items():
    ax.plot(traj_data['lons'], 
            traj_data['lats'],
            color='orange',
            transform=ccrs.PlateCarree(),
            zorder=1,
            label='Trajectory' if traj_num == 1 else "")  # Only label one trajectory

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
plt.title('Fire Locations (June 1-3, 2023) with Forecast Trajectories')
plt.legend()

# Show and save the plot
plt.savefig('fire_locations_plus_fcst_map.png', dpi=300, bbox_inches='tight')