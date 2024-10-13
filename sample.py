import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Sample Data
data = pd.DataFrame({
    'States': ['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu', 'Gujarat'],
    'Count': [100, 80, 120, 70, 90]
})

# Load the shapefile for India states
india_shape = gpd.read_file('india_st.shp')

# Print the columns to identify the correct one for state names
print(india_shape.columns)

# Adjust the state name column as needed (replace 'STATE_NAME' with actual column name)
india_shape['States'] = india_shape['STATE'].astype(str)  # Update accordingly

# Normalize state names to ensure they match
data['States'] = data['States'].str.lower().str.strip()
india_shape['States'] = india_shape['States'].str.lower().str.strip()

# Merge the dataframes
merged = india_shape.set_index('States').join(data.set_index('States'))

# Check the merged data
print(merged[['Count']])  # Should show counts now

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 15))
merged.plot(column='Count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8',
            legend=True, missing_kwds={'color': 'lightgrey', 'label': 'No Data'})

# Set title and remove axis
ax.set_title('State-wise Heatmap (Count)', fontsize=16)
ax.set_axis_off()

# Show the plot
plt.show()
