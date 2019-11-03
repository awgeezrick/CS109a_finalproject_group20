# spotify_database
# Author - Mark McDonald - 2019
# Handles Spotify database queries
# Sets up engine and session

#v1: Initial Release
#v2: Extended for audio_features

import time

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Float, String
from sqlalchemy import MetaData, and_, or_, func,distinct
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Wrapper - displayes time to execute function passed in
def display_time(func):
    start = time.time()
    result = func()
    end = time.time()
    elapsed_time = round(end-start,2)
    print("Time to Execute: {} seconds".format(elapsed_time))
    return result


def get_session(db_path: str):

    # Base type classes can be tied between python and DB tables
    Base = declarative_base()

    # Class that ties Artists class to a table called artists
    class Artists(Base):
        __tablename__ = 'artists'

        artist_uri          = Column(String, primary_key = True)
        followers           = Column(Integer)
        genres              = Column(String)
        artist_name         = Column(String)
        artist_popularity   = Column(Integer)

    # v2: Class that ties Audio_Features class to a table called audio_features
    class Tracks(Base):
        __tablename__='tracks'

        track_uri           = Column(String, primary_key = True)
        artist_uri          = Column(String)
        danceability        = Column(Float)
        energy              = Column(Float)
        key                 = Column(Integer)
        loudness            = Column(Float)
        mode                = Column(Integer)
        speechiness         = Column(Float)
        acousticness        = Column(Float)
        instrumentalness    = Column(Float)
        liveness            = Column(Float)
        valence             = Column(Float)
        tempo               = Column(Float)
        duration_ms         = Column(Integer)
        time_signature      = Column(Integer)
        track_popularity    = Column(Integer)

    # Class that ties Songs class to a table called songs
    # v2: added ForeignKey contraint to track_uri
    class Playlists(Base):
        __tablename__ = 'playlists'

        id                  = Column(Integer, primary_key = True)
        playlist_id         = Column(Integer)
        pos                 = Column(Integer)
        artist_name         = Column(String)
        track_uri           = Column(String)
        artist_uri          = Column(String)
        track_name          = Column(String)
        album_uri           = Column(String)
        duration_ms         = Column(Integer)
        album_name          = Column(String)


    # set attributes for the function so classes can be retrieved
    setattr(get_session, 'Playlists', Playlists)
    setattr(get_session, 'Tracks', Tracks)
    setattr(get_session, 'Artists', Artists)

    # First create the engine
    engine = create_engine('sqlite:///' + db_path,
                           echo=False)

    # Creates an ORM lookup table locally used
    # to map python classes to tables.
    # Any Base objects created not in the DB will create
    # a table in the DB
    Base.metadata.create_all(engine)

    # Create a session instance
    Session = sessionmaker(bind=engine)  # create Session class bound to our DB
    session = Session()  # get a session instance

    return session
