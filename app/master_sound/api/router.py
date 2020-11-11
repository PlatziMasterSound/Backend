from flask import request, Blueprint
from flask_restful import Api

from .resources.user_resource import SignUpResource, LoginResource, UserResource
from .resources.album_resource import AlbumListResource
from .resources.song_resource import SongListResource
from .resources.playlist_resource import PlaylistListResource, PlaylistResource
from .resources.favourite_resource import FavouriteResource

master_sound_api = Blueprint('master_sound_api', __name__)

api = Api(master_sound_api)

api.add_resource(SignUpResource, '/api/auth/signup', endpoint='signup_resource')
api.add_resource(UserResource, '/api/user/<int:user_id>', endpoint='user_resource')
api.add_resource(AlbumListResource, '/api/albums/new-releases', endpoint='albums_list_resource')
api.add_resource(SongListResource, '/api/albums/<album_id>/songs', endpoint='songs_list_resource')
api.add_resource(LoginResource, '/api/auth/login', endpoint='login_resource')
api.add_resource(PlaylistListResource, '/api/playlists/user/<int:user_id>', endpoint='playlist_list_resource')
api.add_resource(PlaylistResource, '/api/playlists/<int:playlist_id>/songs', endpoint='playlist_list_by_id_resource')
api.add_resource(FavouriteResource, '/api/playlists/favourite/user/<int:user_id>', endpoint='playlist_favourite_resource')

