

def get_formatted_feature_df(conn, genres=None):
    import pandas as pd
    from sqlalchemy import create_engine
    
    cursor = conn.cursor()
    
    track_metadata_features = ['tm.title', 'm_term.artist_id', 'tm.artist_name', 'ta.track_id', 'm_term.term', 'ta.duration', 'ta.key music_key', 'ta.loudness', 'ta.mode', 'ta.tempo music_tempo', 'ta.time_signature']
    select_clause = ','.join(track_metadata_features)

    if genres is None:
        genre_where_clause = '''(m_term.term = 'hip hop' OR m_term.term = 'metal')'''
    else:
        genre_where_clause = '''m_term.term IN ({})'''.format(','.join(['\'' + genre + '\'' for genre in genres]))

    where_clause = '''ta.track_id = tm.target_id AND {}'''.format(genre_where_clause)

    query = '''SELECT {} FROM artist_term m_term
                    INNER JOIN track_metadata tm ON tm.artist_id = m_term.artist_id
                    INNER JOIN track_analysis ta ON ta.track_id = tm.target_id
                    WHERE {}; '''.format(select_clause, where_clause)
    
    full_set = pd.read_sql_query(query,conn)
    
    full_set['music_key'] = full_set['music_key'].astype('category')
    full_set['artist_name'] = full_set['artist_name'].str.strip()
    full_set['term'] = full_set['term'].str.strip()
    full_set['title'] = full_set['title'].str.strip()
    
    return full_set


import io
import sys
class IteratorFile(io.TextIOBase):
    
    """ given an iterator which yields strings,
    return a file like object for reading those strings """

    def __init__(self, it):
        self._it = it
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):

        try:
            while self._f.tell() < length:
                self._f.write(next(self._it) + "\n")
                
        except StopIteration as e:
            # soak up StopIteration. this block is not necessary because
            # of finally, but just to be explicit
            pass

        except Exception as e:
            print("uncaught exception: {}".format(e))
            
        finally:
            self._f.seek(0)
            data = self._f.read(length)

            # save the remainder for next read
            remainder = self._f.read()
            self._f.seek(0)
            self._f.truncate(0)
            self._f.write(remainder)
            return data

    def readline(self):
        return next(self._it)
    
def get_lyrics_for_tracks(conn, tracks):
    import pandas as pd
    cursor = conn.cursor()

    cursor.execute('''CREATE TEMP TABLE temp_track_ids ( 
                    track_id character(18)
                   ) ON COMMIT DROP;''')
    cursor.execute('''CREATE INDEX temp_tid_index ON temp_track_ids (track_id);''')

    f = IteratorFile(("{}".format(x) for x in tracks))
    cursor.copy_from(f, 'temp_track_ids', columns=['track_id'])

    lyric_query = '''SELECT * 
                        FROM stopless_lyrics
                        WHERE EXISTS (
                            SELECT 1
                            FROM temp_track_ids
                            WHERE stopless_lyrics.track_id = temp_track_ids.track_id);'''
    lyrics = pd.read_sql_query(lyric_query,conn)
    conn.commit()
    lyrics['word'] = lyrics['word'].str.strip()
    lyrics = lyrics[~lyrics['word'].str.contains('\d')]
    lyrics.set_index('track_id', inplace=True)
    return lyrics

