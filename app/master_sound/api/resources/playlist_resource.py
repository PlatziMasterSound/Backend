from flask import request, jsonify
from flask_restful import Resource

from app.master_sound.api.schemas import PlaylistSchema, SongSchema
from app.master_sound.models import Playlist, User
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

class PlaylistResource(Resource):
    def get(self, playlist_id):
        playlist = Playlist.simple_filter(playlist_id=playlist_id, favourite=0)[0]
        if not playlist:
            raise ObjectNotFound('There was no playlists for this user.')
        songs = playlist.songs
        if not songs:
            raise ObjectNotFound('There were no songs available for the requested playlist')
        result = song_schema.dump(songs)
        return result, 200

    def post(self):
        data = request.get_json()
        playlist = Playlist(**data)

        try:
            playlist.save()
        except Exception as e:
            raise AppErrorBaseClass(f'There was an error while saving the playlist. {e}')

        result = playlist_schema.dump(playlist)
        return result, 200

