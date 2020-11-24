import os
from datetime import timedelta

from flask import request, jsonify
from flask_restful import Resource

from app.master_sound.models import Song, Album
from app.common.error_handling import ObjectNotFound
from app.master_sound.api.schemas import SongSchema

song_schema = SongSchema(exclude=['album'])


class SongListResource(Resource):
    def get(self, spt_album_id):
        album = Album.simple_filter(spt_album_id=spt_album_id)[0]
        if not album:
            raise ObjectNotFound('The requested album does not exist.')
        songs = album.songs
        results = song_schema.dump(songs, many=True)
        for result in results:
            result['spt_album_id'] = album.spt_album_id
        return results, 200

    def post(self):
        data = request.get_json()


