from sqlalchemy import create_engine

conn = create_engine('postgresql://davis:davis_password@localhost:5432/mcnulty').raw_connection()
cursor = conn.cursor()

root_folder = 'converted_files/'


def drop_all_tables():
    cursor.execute('DROP SCHEMA public CASCADE;')
    cursor.execute('CREATE SCHEMA public;')
    conn.commit()
    print('Tables Dropped')


def create_tables():
    cursor.execute('''CREATE TABLE artist ( 
                artist_id character(18) PRIMARY KEY,
                artist_mbid character(36),
                artist_name character(400)
               );''')

    cursor.execute('''CREATE TABLE track ( 
                    track_id character(18) PRIMARY KEY,
                    song_id character(18),
                    artist_name character(400),
                    track_name character(400)
                   );''')

    cursor.execute('''CREATE TABLE track_per_year ( 
                track_id character(18) PRIMARY KEY,
                year smallint,
                artist_name character(400),
                track_name character(400)
               );''')

    cursor.execute('''CREATE TABLE artist_similarity ( 
                target character(18), 
                other_target character(18), 
                PRIMARY KEY(target, other_target)
                );''')

    cursor.execute('''CREATE TABLE track_metadata ( 
                target_id character(18) PRIMARY KEY, 
                title character(400),
                song_id character(18),
                release character(400),
                artist_id character(18),
                artist_mbid character(36),
                artist_name character(400),
                duration double precision,
                artist_familiarity double precision,
                artist_hotttness double precision,
                year smallint
                );''')

    cursor.execute('''CREATE TABLE artist_mbtag ( 
                artist_id character(18), 
                tag character(400)
                );''')

    cursor.execute('''CREATE TABLE artist_term ( 
                artist_id character(18), 
                term character(400)
                );''')
    cursor.execute('''CREATE TABLE track_analysis ( 
                track_id character(18) PRIMARY KEY, 
                danceability double precision,
                duration double precision,
                end_of_fade_in double precision,
                energy double precision,
                key smallint,
                key_confidence double precision,
                loudness double precision,
                mode smallint,
                mode_confidence double precision,
                start_of_fade_out double precision,
                tempo double precision,
                time_signature smallint,
                time_signature_confidence double precision
                    );''')
    #TODO handle dupe song_id
    cursor.execute('''CREATE TABLE song_metadata_hdf5 ( 
                    song_id character(18), 
                    artist_7digitalid integer,
                    artist_familiarity double precision,
                    artist_hotttnesss double precision,
                    artist_id character(18),
                    artist_latitude double precision,
                    artist_location character(500),
                    artist_longitude double precision,
                    artist_mbid character(36),
                    artist_name character(400),
                    artist_playmeid integer,
                    release character(400),
                    release_7digitalid integer,
                    song_hotttnesss double precision,
                    title character(500),
                    track_7digitalid integer
                        );''')

    print('Tables Created')


def populate_tables():
    file_names_table_names = [('CONVERTED_unique_artists.csv', 'artist')]
    file_names_table_names.append(('CONVERTED_unique_tracks.csv', 'track'))
    file_names_table_names.append(('CONVERTED_tracks_per_year.csv', 'track_per_year'))
    file_names_table_names.append(('CONVERTED_subset_artist_similarity||similarity.csv', 'artist_similarity'))
    file_names_table_names.append(('CONVERTED_subset_track_metadata||songs.csv', 'track_metadata'))
    file_names_table_names.append(('CONVERTED_subset_artist_term||artist_mbtag.csv', 'artist_mbtag'))
    file_names_table_names.append(('CONVERTED_subset_artist_term||artist_term.csv', 'artist_term'))
    file_names_table_names.append(('CONVERTED_track_analysis.csv', 'track_analysis'))
    file_names_table_names.append(('CONVERTED_song_metadata.csv', 'song_metadata_hdf5'))

    for file_table_name in file_names_table_names:
        csv_file = root_folder + file_table_name[0]
        with open(csv_file, 'r') as f:
            cmd = 'COPY {} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(file_table_name[1])
            cursor.copy_expert(cmd, f)
            conn.commit()
            print('Filled {} with {}'.format(file_table_name[1], file_table_name[0]))


drop_all_tables()
create_tables()
populate_tables()
