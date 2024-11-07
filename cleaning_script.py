import pandas as pd
import numpy as np

# import excel
# Read the Excel file, skipping the first 9 rows
df = pd.read_excel('CFS DATA SET.xlsx', skiprows=9)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


# Display the first few rows of the DataFrame
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

# Replace items in the 'Common Name' column that match 'Location' in the dictionary
df['Common Name'] = df['Location'].map(location_to_common_name).fillna(df['Common Name'])

# Remove apt and bldg from Location
df['Apt/Building'] = df['Location'].str.extract(r'(?i)((?:apt|bldg).*)', expand=False)
# Remove the extracted substring from Location
df['Location'] = df.apply(lambda row: row['Location'].replace(row['Apt/Building'], '').strip() if pd.notnull(row['Apt/Building']) else row['Location'], axis=1)

# Insert the 'Apt/Building' column at the 9th position
df.insert(9, "Apt/Building", df.pop("Apt/Building"))

# Mark combined incidents
df['Combined'] = df['Incident Type'].str.contains('combined', case=False, regex=True)
df.insert(8,"Combined", df.pop("Combined"))
df['Incident Type'] = df['Incident Type'].str.replace(r'combined', '', case=False, regex=True).str.strip()

df['County'] = 'Prince George\'s County'
df['State'] = 'Maryland'

df.to_csv(file_path, index=False)

print('data cleaned and saved to', file_path)