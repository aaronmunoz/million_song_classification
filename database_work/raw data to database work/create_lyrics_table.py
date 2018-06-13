from sqlalchemy import create_engine

conn = create_engine('postgresql://*****@localhost:5432/mcnulty_songs').raw_connection()
cursor = conn.cursor()


def drop_all_tables():
    cursor.execute('DROP TABLE lyrics;')
    conn.commit()
    print('Tables Dropped')


def create_lyric_tables():
    cursor.execute('''CREATE TABLE lyrics ( 
                track_id character(18),
                word character(60),
                count integer,
                is_test boolean
               );''')

    cursor.execute('''CREATE INDEX track_lyric_index ON lyrics (track_id);''')
    cursor.execute('''CREATE INDEX word_lyric_index ON lyrics (word);''')
    cursor.execute('''CREATE INDEX count_lyric_index ON lyrics (count);''')
    cursor.execute('''CREATE INDEX test_lyric_index ON lyrics (is_test);''')

    conn.commit()
    print('Table Created')


def insert_lyric_csv():
    with open('lyrics.csv', 'r') as f:
        cmd = 'COPY {} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format('lyrics')
        cursor.copy_expert(cmd, f)
        conn.commit()
        print('Filled Lyrics Table')
