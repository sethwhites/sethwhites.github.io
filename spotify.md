# DJ tool with Spotify

## Tool:
I designed a tool to interface with spotify and create a csv that lets me look at metadata for songs. This is very custom. Unfortunately the code is depracated because spotify updated their back end api to hide the metadata that I cared about.  
Code already existed to pop each song but the spotify api didn't like having a request for every song.
## Sample CSV with metadata:
|    | name                                                                 | artist            | danceability | energy | key | mode | instrumentalness | valence | tempo   | id                     | duration_ms | time_signature |
|----|----------------------------------------------------------------------|-------------------|--------------|--------|-----|------|------------------|---------|---------|------------------------|-------------|----------------|
| 0  | Levels                                                               | Nick Jonas        | 0.432        | 0.656  | 5   | 0    | 0.0              | 0.66    | 198.452 | 6pf9datdAtxQj4EU8UYHSx | 167693      | 4              |
| 1  | Lie to Me                                                            | MIKOLAS           | 0.835        | 0.698  | 6   | 1    | 1.88e-06         | 0.664   | 105.997 | 6zBdVVksaTQeAzwfszbovz | 171080      | 4              |
| 2  | Hands Up (feat. DNCE)                                                | Merk & Kremont    | 0.755        | 0.725  | 4   | 0    | 0.0              | 0.558   | 107.996 | 0nlyO7lNTOYB0gjDp7NI7H | 165785      | 4              |
| 3  | Messy                                                                | Kiiara            | 0.893        | 0.456  | 9   | 1    | 0.0              | 0.681   | 108.037 | 0BOEuUKoHdy8in20fG5smd | 169324      | 4              |
| 4  | Blow Your Mind (Mwah)                                                | Dua Lipa          | 0.654        | 0.796  | 2   | 0    | 0.0              | 0.491   | 108.854 | 7kJlTKjNZVT26iwiDUVhRm | 178583      | 4              |
| 5  | Crash                                                                | USHER             | 0.698        | 0.591  | 0   | 1    | 0.00033          | 0.244   | 103.967 | 107ZmaJvvUr4Vi0C8D53R7 | 211387      | 4              |
| 6  | Like It's Over - Glasstempo Remix                                    | Jai Wolf          | 0.553        | 0.322  | 5   | 0    | 0.0746           | 0.17    | 91.965  | 12DpnwP7FwvrQAjwHvs7Aw | 231522      | 4              |
| 7  | Trouble Remix (feat. Wale, Trey Songz, T-Pain, J. Cole & DJ Bay Bay) | Maejor            | 0.596        | 0.8    | 1   | 0    | 2.27e-05         | 0.567   | 193.861 | 7cIqzYC3UcEwUAzlRYIt2F | 238693      | 4              |
| 8  | Up Down (Do This All Day) (feat. B.o.B)                              | T-Pain            | 0.778        | 0.498  | 5   | 0    | 0.0              | 0.464   | 96.995  | 6lbhWl34Il0WXm5pX1fM9E | 231093      | 4              |
| 9  | Down The Road                                                        | C2C               | 0.72         | 0.595  | 2   | 0    | 4.73e-05         | 0.486   | 111.0   | 1x5MjCffpcdHLf65eR9r3T | 207187      | 4              |
| 10 | Lemonade                                                             | Danity Kane       | 0.76         | 0.73   | 3   | 0    | 0.0              | 0.741   | 97.152  | 6CP5Pb9D2LuXHBZvmrnNSz | 264153      | 4              |

## Code:

```python
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


```
