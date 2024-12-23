# README.md

## Overview
This collection of scripts and data files is designed to analyze and visualize air quality data and fire locations during the June 2023 Canadian wildfire smoke event, with a focus on the Central New York region.

## Setup and Execution

### Prerequisites
- Python 3.x
- Conda environment with required packages
- Working directory containing all files

### Installation & Setup
Do this only once:
```bash
# Create and move to working directory
mkdir thesis
cd ~/thesis

# Activate conda environment
conda activate snk29
```

Otherwise, just do this:
```bash
# Navigate to thesis directory
cd ~/thesis

# Activate conda environment
conda activate snk29
```

### Execution Order
1. `python combinedCodeForFigs.py`
   - Creates multiple figures showing PM2.5 data from different sources
   - Outputs: Various .png files showing air quality measurements

2. `python fireDataPlus2Trajectories.py`
   - Plots fire locations with back trajectories for both Ithaca and Syracuse
   - Outputs: 'fire_locations_map.png'

3. `python fireDataPlusForecast.py`
   - Creates map with fire locations and forecast trajectories
   - Outputs: 'fire_locations_plus_fcst_map.png'

## Data Files
- `NFDB_filtered_point_20240613.txt`: Fire location data
- `syracuse_ithaca_outdoor_pm25_june_2023.csv`: PM2.5 measurements
- `syracuse_ithaca_outdoor_pm25_june_2023_stats.csv`: Statistical summaries
- Trajectory files:
  - `tdump.154659.txt`
  - `tdump.138880.txt`
  - `tdump.138766.txt`

## Easy Modifications

### Map Projection Changes
To modify the map extent, locate these lines in the scripts:
```python
ax.set_extent([-90, -63, 36, 58], crs=ccrs.PlateCarree())
```
Adjust the numbers to change the view:
- First two numbers: longitude range (West to East)
- Last two numbers: latitude range (South to North)

### Trajectory Colors
Find lines containing `color='orange'` or `color='coral'` and change to any color name:
```python
ax.plot(..., color='blue')  # Try: 'red', 'green', 'purple', etc.
```

### Figure Sizes
Look for lines like:
```python
plt.figure(figsize=(12, 8))  # Change numbers for different dimensions
```
- First number: width in inches
- Second number: height in inches

### Font Sizes
Locate text elements with `fontsize` parameter:
```python
plt.title('Your Title', fontsize=14)  # Increase/decrease number
plt.xlabel('Date', fontsize=12)
```

### Using Different Trajectories
1. Add new trajectory files to working directory
2. Modify the filename in the `read_traj_file()` function call:
```python
trajectories = read_traj_file('your_new_trajectory.txt')
```

### Other Common Modifications
- Change marker styles: Look for `'o'` in plot commands and replace with other markers (`'s'` for squares, `'^'` for triangles)
- Adjust plot transparency: Add `alpha=0.5` to plot commands (0.0 to 1.0)
- Modify grid appearance: Change `alpha=0.3` in `grid(True, alpha=0.3)`
- Change line thickness: Add or modify `linewidth=2` in plot commands

## Tips
- Always make a backup of original files before making changes
- Test small changes one at a time
- Use print statements to debug if needed
- Most color names from CSS will work (e.g., 'steelblue', 'darkred')
- Save intermediate versions of your modifications

## Common Issues
- If map appears blank: Check coordinate ranges in `set_extent()`
- If trajectories don't show: Verify file paths and names
- If colors don't work: Ensure color names are spelled correctly
