
import csv
import pandas as pd
import spotipy as spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

client_id = "9e62996822a340c19e80e793d3e94f09"
client_secret = "1fa0af23e3184a86adf04cdab9465bb6"

client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def get_playlist_track_infos(playlist_link, sp, output_file_name):
    '''Extract track information of each track in the playlist, 
    and create a dataframe with those information'''
    offset = 0
    tracks = []
    playlist_uri = playlist_link.split("/")[-1]
    while True:
        content = sp.playlist_tracks(playlist_uri, fields = None, limit = 100, offset = offset, market = None)
        tracks += content['items']
        # Create a if-else loop so that spotify can extract information more than 100
        if content['next'] is not None:
            offset += 1000
        else:
            break
            
    track_info_list = []
    for track in tracks:
        # Track URI
        track_uri = track["track"]["uri"]
        #Track name
        track_name = track["track"]["name"]

        #Main Artist
        artist_name = track["track"]["artists"][0]["name"]

        #Popularity of the track
        track_pop = track["track"]["popularity"]

        track_info_list.append([track_uri, track_name, artist_name, track_pop])

    df = pd.DataFrame(track_info_list, columns = ['track_uri', 'track_name', 'artist', 'track_popularity'])
    df.to_csv("{}.csv".format(output_file_name), index = False)
    
    
    
    

def get_playlist_audio_features(df, sp, output_file_name):
    '''Extract audio features of each track in specified dataframe, 
    then create a dataframe with those information'''
    track_list = df['track_uri'].to_list()
    features_list = []
    for j in track_list:
        features = sp.audio_features(j)[0]
        features_list.append([j, features['danceability'], features['valence'], features['energy'],
                            features['tempo'], features['loudness'], features['speechiness'], 
                            features['instrumentalness'], features['liveness'], 
                            features['acousticness'], features['key']])

    df = pd.DataFrame(features_list, columns = ['track_uri', 'danceability', 'valence', 'energy',
                                               'tempo', 'loudness', 'speechiness', 
                                                'instrumentalness', 'liveness', 
                                               'acousticness', 'key'])
    df.to_csv("{}.csv".format(output_file_name), index = False)

links = ["https://open.spotify.com/playlist/37i9dQZF1DXe2bobNYDtW8", "https://open.spotify.com/playlist/37i9dQZF1DWVRSukIED0e9", "https://open.spotify.com/playlist/2fmTTbBkXi8pewbUvG3CeZ", 
         "https://open.spotify.com/playlist/5GhQiRkGuqzpWZSE7OU4Se", "https://open.spotify.com/playlist/4hMcqod7ERKJ9mtjgdimeV"]



get_playlist_track_infos(links[4], sp, '2022')
track_22 = pd.read_csv('2022.csv')

get_playlist_audio_features(track_22, sp, 'audio_22')
audio_22 = pd.read_csv('audio_22.csv')