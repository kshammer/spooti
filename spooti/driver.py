import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secret import client_id
from secret import client_secret
import queue
from spooti import PriorityQueue
client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager =client_credentials_manager)


def how_separate(artist_info):
    artist_ids = get_artist_ids(artist_info['start_info'], artist_info['finish_info'])
    q = queue.Queue()
    q.put(artist_ids['start_id'])
    v = set()
    depth = 0
    while not q.empty():
        depth += 1
        current = q.get()
        if current in v:
            continue
        if current == artist_ids['finish_id']:
            return depth
        v.add(current)
        current_artist = sp.artist(current)
        artist_name = current_artist['name']
        print('Current node is {}'.format(artist_name))
        related_info = sp.artist_related_artists(current)
        related_ids = map(lambda x: x['id'], related_info['artists']) # cool little lambda to get all the ids
        for artist in list(related_ids):
            if artist not in v:
                q.put(artist)


def better_how_separate(artist_info):
    pq = PriorityQueue.PriorityQueue()
    artist_bases = get_artist_bases(artist_info['start_info'], artist_info['finish_info'])
    pq.setBase(artist_bases['finish_base'])
    artist_ids = get_artist_ids(artist_info['start_info'], artist_info['finish_info'])
    pq.insert(artist_bases['start_base'], artist_ids['start_id'])
    v = set()
    depth = 0
    while not pq.isEmpty():
        depth += 1
        current = pq.pop()
        current = current[1] # just artist id
        if current in v:
            continue
        if current == artist_ids['finish_id']:
            return depth
        v.add(current)
        current_artist = sp.artist(current)
        artist_name = current_artist['name']
        print('Current node is {}'.format(artist_name))
        related_info = sp.artist_related_artists(current)
        related_ids_info = map(lambda x: (x['id'], x['genres']), related_info['artists']) # both id and genres
        for artist in list(related_ids_info):
            if artist[0] not in v:
                pq.insert(artist[1], artist[0])


def get_artist_info(starter='Death Grips', end = 'Kero Kero Bonito'):
    start_info = sp.search(starter, type='artist')
    finish_info = sp.search(end, type='artist')
    return {'start_info': start_info, 'finish_info': finish_info}


def get_artist_ids(start_info, finish_info):
    start_id = start_info['artists']['items'][0]['id']
    finish_id = finish_info['artists']['items'][0]['id']
    return {'start_id': start_id, 'finish_id': finish_id}


def get_artist_bases(start_info, finish_info):
    start_base = start_info['artists']['items'][0]['genres']
    finish_base = finish_info['artists']['items'][0]['genres']
    return {'start_base': start_base, 'finish_base': finish_base}


if __name__ == '__main__':
    artist_info = get_artist_info()
    lame = how_separate(artist_info)
    print('finished bfs')
    directed = better_how_separate()
    print('Artists needed using normal bfs {}'.format(lame))
    print('Artists needed using genres metric {}'.format(directed))