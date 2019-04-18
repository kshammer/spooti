import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secret import client_id
from secret import client_secret
import queue
import pprint as pp
from spooti import PriorityQueue
import random
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def how_separate(artist_info):
    artist_ids = get_artist_ids(
        artist_info['start_info'], artist_info['finish_info'])
    q = queue.Queue()
    q.put((artist_ids['start_id'], 0))
    v = set()
    artist_seen = 0
    while not q.empty():
        artist_seen += 1
        current = q.get()
        if current[0] in v:
            continue
        if current[0] == artist_ids['finish_id']:
            return artist_seen, current[1]
        v.add(current[0])
        current_artist = sp.artist(current[0])
        artist_name = current_artist['name']
        print('Current node is {} and depth {}'.format(
            artist_name, current[1]))
        related_info = sp.artist_related_artists(current[0])
        # cool little lambda to get all the ids
        related_ids = map(lambda x: x['id'], related_info['artists'])
        depth = current[1] + 1
        for artist in list(related_ids):
            if artist not in v:
                q.put((artist, depth))


def better_how_separate(artist_info):
    pq = PriorityQueue.PriorityQueue()
    artist_bases = get_artist_bases(
        artist_info['start_info'], artist_info['finish_info'])
    pq.setBase(artist_bases['finish_base'])
    artist_ids = get_artist_ids(
        artist_info['start_info'], artist_info['finish_info'])
    pq.insert(artist_bases['start_base'], artist_ids['start_id'], 0)
    v = set()
    artist_dict = dict()
    artist_seen = 0
    while not pq.isEmpty():
        artist_seen += 1
        current = pq.pop()
        current_id = current[1]  # just artist id
        if current_id in v:
            continue
        if current_id == artist_ids['finish_id']:
            return artist_seen, current[3], artist_dict
        v.add(current_id)
        current_artist = sp.artist(current_id)
        artist_name = current_artist['name']
        print('Current node is {} and depth {}'.format(
            artist_name, current[3]))
        related_info = sp.artist_related_artists(current_id)
        # both id and genres
        related_ids_info = map(lambda x: (
            x['id'], x['genres']), related_info['artists'])
        # i don't even know if this works correctly with the pq
        depth = current[3] + 1
        artist_dict[artist_name] = {
            "id": current_id,
            "distance": depth,
            "related": []
        }
        for artist in list(related_ids_info):
            if artist[0] not in v:
                pq.insert(artist[1], artist[0], depth)
                artist_dict[artist_name]['related'].append(artist[0])


def get_artist_info(starter='Death Grips', end='Kero Kero Bonito'):
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


def create_random_playlist(artists):
    related_artist = []
    depth = 1
    cool = [v for v in artists.values() if depth in v.values()
            ]  # I don't know what this does
    rand_artist = random.choice(cool)
    related_artist.append(rand_artist['id'])
    while True:
        depth += 1
        cool = [v for v in artists.values() if depth in v.values()]
        if cool == []:
            break
        rand_artist = random.choice(cool)
        related_artist.append(rand_artist['id'])

    print(related_artist)


if __name__ == '__main__':
    artist_info = get_artist_info()
    directed = better_how_separate(artist_info)
    print('Artists needed using genres metric {} and furthest depth {}'.format(
        directed[0], directed[1]))
    create_random_playlist(directed[2])
