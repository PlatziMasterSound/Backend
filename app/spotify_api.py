import base64
import os

import requests
from app.common.error_handling import AppErrorBaseClass


def get_token():
    BASE_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    CLIENT_ID = 'aba92b636b61480c992f35aa022405f7'
    CLIENT_SECRET = '1d4db40d8e304d43bce78d5bea3d9751'
    client_str = f'{CLIENT_ID}:{CLIENT_SECRET}'
    client_encode = base64.b64encode(client_str.encode('utf8'))
    client_encode = str(client_encode, 'utf8')
    params = {'grant_type': 'client_credentials'}
    headers = {'Authorization': f'Basic {client_encode}'}
    r = requests.post(BASE_TOKEN_URL, data=params, headers=headers)
    if r.status_code == 200:
        os.environ['SPOTIFY_TOKEN'] = r.json()['access_token']
        return
    else:
        raise AppErrorBaseClass('There was an error calling Spotify token.')

