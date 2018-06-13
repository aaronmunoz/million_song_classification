import pandas as pd
import os

IS_SUBSET = True

root = ''
new_file_directory = root + 'converted_files/'
file_name = 'msd_summary_file.h5'

prefix = ''
if IS_SUBSET:
    prefix = 'subset_'

file_name = root + prefix + file_name

if not os.path.exists(new_file_directory):
    os.makedirs(new_file_directory)


track_analysis = '/analysis/songs'

print('Fetching Group: {}'.format(track_analysis))
df = pd.read_hdf(file_name, key=track_analysis, mode='r')
df.set_index('track_id', inplace=True)

analysis_columns_to_keep = ['danceability', 'duration',
       'end_of_fade_in', 'energy', 'key', 'key_confidence', 'loudness', 'mode',
       'mode_confidence', 'start_of_fade_out', 'tempo', 'time_signature',
       'time_signature_confidence']

csv_file_name = new_file_directory + 'CONVERTED_track_analysis.csv'
print('Saving: {}'.format(csv_file_name))
df[analysis_columns_to_keep].to_csv(csv_file_name)
print('Saving: {} Complete'.format(csv_file_name))

song_metadata = '/metadata/songs'

print('Fetching Group: {}'.format(song_metadata))
df = pd.read_hdf(file_name, key=song_metadata, mode='r')
df.set_index('song_id', inplace=True)

metadata_columns_to_keep = ['artist_7digitalid', 'artist_familiarity',
       'artist_hotttnesss', 'artist_id', 'artist_latitude', 'artist_location',
       'artist_longitude', 'artist_mbid', 'artist_name', 'artist_playmeid',
       'release',
       'release_7digitalid', 'song_hotttnesss', 'title',
       'track_7digitalid']

csv_file_name = new_file_directory + 'CONVERTED_song_metadata.csv'
print('Saving: {}'.format(csv_file_name))
df[metadata_columns_to_keep].to_csv(csv_file_name)
print('Saving: {} Complete'.format(csv_file_name))
