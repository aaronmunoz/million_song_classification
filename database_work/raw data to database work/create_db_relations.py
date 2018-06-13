from sqlalchemy import create_engine

conn = create_engine('postgresql://*****@mcnulty.cmelew2b5zmm.us-east-1.rds.amazonaws.com:5432/mcnultysongs').raw_connection()
cursor = conn.cursor()


def create_references():
    cursor.execute('''alter table track_metadata 
                add constraint fk_track_metadata_artist
                foreign key (artist_id) 
                REFERENCES artist (artist_id);''')


create_references()
