from flask import request, jsonify
from flask_restful import Resource

from app.master_sound.api.schemas import PlaylistSchema, SongSchema
from app.master_sound.models import Playlist, User, Song
from app.common.error_handling import ObjectNotFound, AppErrorBaseClass

playlist_schema = PlaylistSchema()
song_schema = SongSchema(exclude=['album'])


class PlaylistListResource(Resource):
    def get(self, user_id):
        user = User.get_by_id(user_id)
        if not user:
            raise ObjectNotFound('There was no user for the requested id.')
        playlists = Playlist.simple_filter(user_id=user_id, favourite=0)
        if not playlists:
            raise ObjectNotFound('There were no playlists for the requested user.')
        results = playlist_schema.dump(playlists, many=True)
        return results, 200

    def post(self, user_id):
        user = User.get_by_id(user_id)
        if not user:
            raise ObjectNotFound('There was no user for the requested id.')
        data = request.get_json()
        playlist = Playlist(**data)
        try:
            user.playlists.append(playlist)
            user.save()
        except Exception as e:
            raise AppErrorBaseClass('There was an error while saving the playlist.')
        result = playlist_schema.dump(playlist)
        print(playlist_schema.dump(user.playlists, many=True))
        return result, 201


class PlaylistResource(Resource):
    def get(self, playlist_id):
        playlist = Playlist.simple_filter(playlist_id=playlist_id, favourite=0)[0]
        if not playlist:
            raise ObjectNotFound('There was no playlists for this user.')
        songs = playlist.songs
        if not songs:
            raise ObjectNotFound('There were no songs available for the requested playlist')
        result = song_schema.dump(songs, many=True)
        return result, 200

    def post(self, playlist_id):
        playlist = Playlist.get_by_id(playlist_id)
        if not playlist:
            raise ObjectNotFound('There was no playlist for the requested id.')
        data = request.get_json()
        song = Song.get_by_id(data['song_id'])
        try:
            playlist.songs.append(song)
            playlist.save()
        except Exception as e:
            raise AppErrorBaseClass(f'There was an error while saving the playlist. {e}')

        result = playlist_schema.dump(playlist)
        return result, 201

