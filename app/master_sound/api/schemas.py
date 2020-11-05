from marshmallow import fields

from app.ext import ma


class UserSchema(ma.Schema):
    user_id = fields.Integer(dump_only=True)
    given_name = fields.String()
    last_name = fields.String()
    email = fields.String()
    password = fields.String()
    country_id = fields.Integer()
    image_url = fields.String()
    sex = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    active = fields.Integer()
    country = fields.Nested('CountrySchema')


class CountrySchema(ma.Schema):
    country_id = fields.Integer(dump_only=True)
    iso = fields.String()
    name = fields.String()
    spanish_name = fields.String()


class AlbumSchema(ma.Schema):
    album_id = fields.Integer(dump_only=True)
    spt_album_id = fields.String()
    cover_image_url = fields.String()
    album_name = fields.String()
    songs = fields.Nested('SongSchema', many=True)
    artists = fields.Nested('ArtistSchema', many=True)


class ArtistSchema(ma.Schema):
    artist_id = fields.Integer(dump_only=True)
    spt_artist_id = fields.String()
    cover_image_url = fields.String()
    artist_name = fields.String()


class SongSchema(ma.Schema):
    song_id = fields.Integer(dump_only=True)
    spt_song_id = fields.String()
    song_name = fields.String()
    spt_album_id = fields.Integer()
    duration = fields.String()
    sound_url = fields.String()
    order_number = fields.Integer()
    album = fields.Nested('AlbumSchema')


class PlaylistSchema(ma.Schema):
    playlist_id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    playlist_name = fields.String()
    favourite = fields.Integer()
    songs = fields.Nested('SongSchema', many=True)

