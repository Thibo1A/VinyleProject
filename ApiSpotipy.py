import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id= '9217a209a079409c85429e564f8c96a8'

client_secret = '6c0c1f30ae974365b7c00dce4f1e278a'

redirect_uri="http://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,client_secret,redirect_uri))

results = sp.search(q='year:2022', type='track', limit=50)

while results:
    tracks = results['tracks']['items']
    for track in tracks:
        print(track['name'], track['album']['name'], track['duration_ms'], track['popularity'])
    results = sp.next(results) if results['tracks']['next'] else None