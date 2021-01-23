import os

from flask import request, jsonify
from flask_restful import Resource
import requests

from app.master_sound.api.schemas import AlbumSchema, ArtistSchema, SongSchema
from app.master_sound.models import Album, Artist, Song
from app.spotify_api import get_token
from app.common.error_handling import AppErrorBaseClass

album_schema = AlbumSchema(exclude=['songs'])


class AlbumListResource(Resource):
    def get(self):
        # albums = Album.get_all().order_by(Album.created_at, ascending=True)[:15]
        albums = Album.query.order_by(Album.created_at.desc()).slice(0, 16).all()
        results = album_schema.dump(albums, many=True)
        for result in results:
            result['artists'] = [result['artists'][0]]
        return results, 200

    def post(self):
        data = request.get_json()
        for _json in data:
            if Album.simple_filter(spt_album_id=_json['spt_album_id']):
                print('Already on the database.')
                continue
            album = Album(cover_image_url=_json['cover_image_url'], spt_album_id=_json['spt_album_id'], album_name=_json['album_name'])
            for artist in _json['artists']:
                try:
                    new_artist = Artist.simple_filter(spt_artist_id=artist['spt_artist_id'])
                    if new_artist:
                        new_artist = new_artist[0]
                        album.artists.append(new_artist)
                    else:
                        new_artist = Artist(spt_artist_id=artist['spt_artist_id'], artist_name=artist['artist_name'], cover_image_url=artist['cover_image_url'])
                        album.artists.append(new_artist)
                except Exception as e:
                    print(e)
                    raise AppErrorBaseClass(f'Error: {e}')
            for song in _json['songs']:
                if Song.simple_filter(spt_song_id=song['spt_song_id']):
                    continue
                try:
                    new_song = Song(spt_song_id=song['spt_song_id'], song_name=song['song_name'], duration=song['duration'], order_number=song['order_number'], sound_url=song['sound_url']) # Hold
                    album.songs.append(new_song)
                except Exception as e:
                    print(e)
                    raise AppErrorBaseClass(f'Error saving song. {e}')
            print(album)
            try:
                album.save()
            except Exception as e:
                print(e)
                raise AppErrorBaseClass(e)
        return {'msg': 'Your albums were saved succesfully.'}, 201

