from datetime import datetime

import requests

from app.db import db, BaseModelMixin

albums_artists = db.Table(
        'albums_artists',
        db.Model.metadata,
        db.Column('albums_artists_id', db.Integer, primary_key=True),
        db.Column('artist_id', db.Integer, db.ForeignKey('artists.artist_id', ondelete='CASCADE'), nullable=False),
        db.Column('album_id', db.Integer, db.ForeignKey('albums.album_id', ondelete='CASCADE'), nullable=False)
        )

playlists_songs = db.Table(
        'playlists_songs',
        db.Model.metadata,
        db.Column('playlists_songs_id', db.Integer, primary_key=True),
        db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.playlist_id', ondelete='CASCADE'), nullable=False),
        db.Column('song_id', db.Integer, db.ForeignKey('songs.song_id', ondelete='CASCADE'), nullable=False)
        )

played_songs = db.Table(
        'played_songs',
        db.Column('played_song_id', db.Integer, primary_key=True),
        db.Column('song_id', db.Integer, db.ForeignKey('songs.song_id', ondelete='CASCADE',), nullable=False),
        db.Column('user_id', db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE',), nullable=False),
        db.Column('created_at', db.DateTime, default=datetime.utcnow),
        db.Column('updated_at', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
        db.Column('active', db.Integer, default=1)
        )


class Country(db.Model, BaseModelMixin):
    __tablename__ = 'countries'

    country_id = db.Column(db.Integer, primary_key=True)
    iso = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    spanish_name = db.Column(db.String(45), nullable=False)
    users = db.relationship('User', back_populates='country', cascade='all, delete, delete-orphan', passive_deletes=True)


class User(db.Model, BaseModelMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    given_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.country_id', ondelete='CASCADE'), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Integer, nullable=False, default=1)
    country = db.relationship('Country', back_populates='users')
    played_songs = db.relationship('Song', back_populates='playing_users', secondary=played_songs, passive_deletes=True)
    playlists = db.relationship('Playlist', back_populates='user')


class Album(db.Model, BaseModelMixin):
    __tablename__ = 'albums'

    album_id = db.Column(db.Integer, primary_key=True)
    cover_image_url = db.Column(db.String(100))
    spt_album_id = db.Column(db.String(30), nullable=False, unique=True)
    album_name = db.Column(db.String(80), nullable=False)
    songs = db.relationship('Song', back_populates='album', cascade='all, delete, delete-orphan', passive_deletes=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Integer, default=1)
    artists = db.relationship('Artist', back_populates='albums', secondary=albums_artists, cascade='all, delete')


class Artist(db.Model, BaseModelMixin):
    __tablename__ = 'artists'

    artist_id = db.Column(db.Integer, primary_key=True)
    spt_artist_id = db.Column(db.String(30), nullable=False, unique=True)
    artist_name = db.Column(db.String(50), nullable=False)
    cover_image_url = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Integer, default=1)
    albums = db.relationship('Album', back_populates='artists', secondary=albums_artists, passive_deletes=True)


class Song(db.Model, BaseModelMixin):
    __tablename__ = 'songs'

    song_id = db.Column(db.Integer, primary_key=True)
    spt_song_id = db.Column(db.String(30), nullable=False, unique=True)
    song_name = db.Column(db.String(120), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id', ondelete='CASCADE'), nullable=False)
    order_number = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.String(6), nullable=False)
    sound_url = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Integer, default=1)
    album = db.relationship('Album', back_populates='songs')
    playlists = db.relationship('Playlist', back_populates='songs', secondary=playlists_songs, cascade='all, delete')
    playing_users = db.relationship('User', back_populates='played_songs', secondary=played_songs, cascade='all, delete')


class Playlist(db.Model, BaseModelMixin):
    __tablename__ = 'playlists'

    playlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    playlist_name = db.Column(db.String(50), nullable=False)
    favourite = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Integer, default=1)
    user = db.relationship('User', back_populates='playlists')
    songs = db.relationship('Song', back_populates='playlists', secondary=playlists_songs, passive_deletes=True)

