import pandas as pd
import sqlite3
import os

IS_SUBSET = True
new_file_directory = 'converted_files'


class MillionSongTextToCSV:

    def __init__(self, name, columns, index, columns_to_drop=None):
        self.name = name
        self.columns = columns
        self.index = index

        self.columns_to_drop = columns_to_drop

    def get_txt_name(self):
        return self.name + '.txt'

    Seperator = '<SEP>'


class MillionSongTableToCSV:
    def __init__(self, db_name, table_names, index):
        self.db_name = db_name
        self.table_names = table_names
        self.index = index

    def get_db_name(self):
        return self.db_name + '.db'


prefix = ''
if IS_SUBSET:
    prefix = 'subset_'

if not os.path.exists(new_file_directory):
    os.makedirs(new_file_directory)

##################################################################################################
#######
####### Convert Text Files
#######
##################################################################################################

tracks_per_year = MillionSongTextToCSV('tracks_per_year', ['year', 'track_id', 'artist_name', 'title'], 'track_id')
unique_artists = MillionSongTextToCSV('unique_artists', ['artist_id', 'artist_mbid', 'track_id', 'artist_name'], 'artist_id')
unique_artists.columns_to_drop = ['track_id']
unique_tracks = MillionSongTextToCSV('unique_tracks', ['track_id', 'song_id', 'artist_name', 'title'], 'track_id')

files_to_convert = [tracks_per_year, unique_artists, unique_tracks]

for converter in files_to_convert:
    df = pd.read_csv(prefix + converter.get_txt_name(), sep = MillionSongTextToCSV.Seperator,
                     names=converter.columns, index_col=converter.index)
    if converter.columns_to_drop:
        df.drop(converter.columns_to_drop, axis=1, inplace=True)
    file_name = new_file_directory + '/CONVERTED_' + converter.name + '.csv'
    df.to_csv(file_name)
    print('Created: {}'.format(file_name))


##################################################################################################
#######
####### Convert DB Files
#######
##################################################################################################

artist_similarity = MillionSongTableToCSV(prefix + 'artist_similarity', ['similarity'], 'target')
track_metadata = MillionSongTableToCSV(prefix + 'track_metadata', ['songs'], 'track_id')
artist_terms = MillionSongTableToCSV(prefix + 'artist_term', ['artist_term','artist_mbtag'], 'artist_id')

converters = [artist_similarity, track_metadata, artist_terms]

for converter in converters:
    conn = sqlite3.Connection(converter.get_db_name())

    for table in converter.table_names:
        query = '''SELECT * FROM {};'''.format(table)

        df = pd.read_sql(query, conn, index_col=converter.index)
        file_name = new_file_directory + '/CONVERTED_{}||{}.csv'.format(converter.db_name, table)
        df.to_csv(file_name)
        print('Created: {}'.format(file_name))
