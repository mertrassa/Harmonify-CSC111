"""CSC111 Data"""
import pandas as pd

df = pd.read_csv('pre_processed_all_songs.csv')

# Remove duplicates (keep the first occurrence)
df = df.drop_duplicates()

# Group by 'track_name' and keep the first occurrence (highest popularity for each track)
df_sorted = df.groupby('track_name', sort=False).first().reset_index()

# Sort by 'popularity' in descending order and keep the top 200
df_sorted = df_sorted.sort_values(by='popularity', ascending=False).head(200)

# Drop unnecessary columns from the sorted dataframe
df_sorted = df_sorted.drop(
    columns=['track_id', 'album_name', 'explicit', 'danceability', 'popularity', 'energy', 'time_signature', 'tempo',
             'valence', 'liveness', 'instrumentalness', 'acousticness', 'speechiness', 'mode', 'key', 'loudness'],
    errors='ignore'  # Ignore if any column is missing
)

# Reset the index and make it start from 1
df_sorted.reset_index(drop=True, inplace=True)
df_sorted.index += 1  # Start the index from 1

if 'Unnamed: 0' in df.columns:
    df_sorted = df_sorted.drop('Unnamed: 0', axis=1)


# Save the sorted CSV to a new file
df_sorted.to_csv('songs_by_popularity.csv', index_label='Rank', header=False)
