import spotipy, requests, urllib3
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import sys

session = requests.Session()

retry = urllib3.Retry(
    total=0,
    connect=None,
    read=0,
    allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE']),
    status=0,
    backoff_factor=0.3,
    status_forcelist=(429, 500, 502, 503, 504),
    respect_retry_after_header=True  # <---
)

adapter = requests.adapters.HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def generate_token():
    client_id = 'na'
    client_secret = 'na'
    redirect_uri = 'http://localhost:8080'
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(client_id,
                                            client_secret,
                                            redirect_uri,
                                            scope="user-library-read"
        ),
    )
    return sp


username = '1243216393'
playlist_id = '5F4Mdaga8J3O4KUDZBiwMu'

sp = generate_token()
playlist = sp.user_playlist_tracks(username, playlist_id)
playlist_size = playlist['total']
j = 0   # for display
k = 0   # for flag creating dataframe
n = 0   # songs counter
new_dict = {}
# while playlist['next']:
while True:     # it doesn't grab the last page if I don't include a while do loop.
    songs = playlist['items']
    ids = []
    title = []
    artist_list = []
    features = []
    for i in range(len(songs)):
        if(songs[i]["track"]["id"] is not None):
            n+=1    # song count+1
            ids.append(songs[i]["track"]["id"])
            title.append(songs[i]["track"]["name"])
            m=0
            for artist in songs[i]["track"]["artists"]: # i don't know how to just grab the first item in artists so this is what I did
                m+=1
                if m==1:
                    artist_list.append(artist['name'])
    features = sp.audio_features(ids)
    if k == 0:
        k+=1
        df = pd.DataFrame(features)
        df.insert(0, 'name', title, True)
        df.insert(1, 'artist', artist_list, True)
    else:
        df_temp = []
        df_temp = pd.DataFrame(features)
        df_temp.insert(0, 'name', title)
        df_temp.insert(1, 'artist', artist_list, True)
        df = pd.concat([df, df_temp], ignore_index=True)
    playlist = sp.next(playlist)
    j += 1
    print('\r' + 'loaded ' + str(j) + ' pages and ' + str(n) +'/' + str(playlist_size) + ' tracks' , end = '')  #displays song count
    if playlist is None:
        break

# need to edit duration_ms to mm:ss string

df = df.drop(['liveness', 'acousticness', 'loudness', 'speechiness', 'type', 'uri', 'track_href', 'analysis_url'], axis=1)
df.to_csv(r'./playlist_info.csv', sep=',', encoding='utf-8', header='true')


# wcs_2022_url = 'https://open.spotify.com/playlist/5F4Mdaga8J3O4KUDZBiwMu?si=1ff7aa486341466c'
# greg_playlist = 'https://open.spotify.com/playlist/1NAou1VNqaIW48GOw7Dm8C?si=a230c084894e4aa7'

