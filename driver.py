import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secret import client_id
from secret import client_secret
import queue

client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager =client_credentials_manager)


def how_separate(starter='Death Grips', end = 'Kero Kero Bonito'):
    start_info = sp.search(starter, type='artist')
    finish_info = sp.search(end, type='artist')
    start_id = start_info['artists']['items'][0]['id']
    finish_id = finish_info['artists']['items'][0]['id']
    q = queue.Queue()
    q.put(start_id)
    v = set()
    depth = 0
    while not q.empty():
        depth += 1 
        current = q.get()
        if current in v:
            continue
        if current == finish_id:
            return depth
        v.add(current)
        artist_info = sp.artist(current)
        artist_name = artist_info['name']
        print("Current node is {}".format(artist_name))
        related_info = sp.artist_related_artists(current)
        related_ids = map(lambda x: x['id'], related_info['artists']) # cool little lambda to get all the ids 
        for artist in list(related_ids):
            if artist not in v:
                q.put(artist)
    

if __name__ == '__main__':
    print("The distance between two artists is {}".format(how_separate()))