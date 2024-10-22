import pandas as pd
import numpy as np

#Put all cleaning steps here
df = pd.read_csv('cfs_data.csv')

df.head()

file_path = 'cfs_data_cleaned.csv'

# Remove Appox Loc from Location
df['Location'] = df['Location'].str.replace('Approx Loc:', '', case=False)

# Filter Wb and Eb from Location
df['Location'] = df['Location'].str.replace(' Wb', '', case=False)
df['Location'] = df['Location'].str.replace(' Eb', '', case=False)

# Replace ' / ' with ' & ' in Location
df['Location'] = df['Location'].str.replace(' / ', ' & ', case=False)

# Group by 'Location' and 'Common Name' and count occurrences
location_common_name_counts = df.groupby(['Location', 'Common Name']).size().reset_index(name='count')

# Filter out 'Common Name' that appears only once for each 'Location'
filtered_counts = location_common_name_counts[location_common_name_counts['count'] > 1]

# Find the most frequent 'Common Name' for each 'Location'
most_frequent_common_name = filtered_counts.loc[filtered_counts.groupby('Location')['count'].idxmax()]

# Create a dictionary with 'Location' as the key and the most frequent 'Common Name' as the value
location_to_common_name = most_frequent_common_name.set_index('Location')['Common Name'].to_dict()

print(location_to_common_name)

# Replace items in the 'Common Name' column that match 'Location' in the dictionary
df['Common Name'] = df['Location'].map(location_to_common_name).fillna(df['Common Name'])

# Remove apt and bldg from Location
df['Unit'] = df['Location'].str.extract(r'(?i)((?:apt|bldg)\s+\d+)', expand=False)
df.insert(9,"Unit", df.pop("Unit"))

df['Combined'] = df['Incident Type'].str.contains('combined', case=False, regex=True)
df.insert(8,"Combined", df.pop("Combined"))
df['Incident Type'] = df['Incident Type'].str.replace(r'combined', '', case=False, regex=True).str.strip()

df.to_csv(file_path, index=False)


df.head()