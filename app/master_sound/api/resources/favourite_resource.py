from flask import request, jsonify
from flask_restful import Resource

from app.common.error_handling import ObjectNotFound, AppErrorBaseClass
from app.master_sound.models import Playlist, Song
from app.master_sound.api.schemas import PlaylistSchema, SongSchema

playlist_schema = PlaylistSchema()
song_schema = SongSchema(exclude=['album'])


class FavouriteResource(Resource):
    def get(self, user_id):
        playlist = Playlist.simple_filter(user_id=user_id, favourite=1)[0]
        if not playlist:
            raise ObjectNotFound('There was no user for the requested id.')
        songs = playlist.songs
        results = song_schema.dump(songs, many=True)
        return results, 200
    
    def post(self, user_id):
        playlist = Playlist.simple_filter(user_id=user_id, favourite=1)[0]
        if not playlist:
            raise ObjectNotFound('There was no user for the requested id.')
        data = request.get_json()
        song_id = data['song_id']
        song = Song.get_by_id(song_id)
        if not song:
            raise ObjectNotFound('There was no song for the requested id.')
        try:
            playlist.songs.append(song)
            playlist.save()
        except Exception as e:
            print(e)
            raise AppErrorBaseClass('There was an error saving the song.')
        result = playlist_schema.dump(playlist)
        return result, 201

