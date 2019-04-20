from pyramid.view import view_config
from pyramid.response import Response

from spooti.driver import Utils 

@view_config(route_name='connect')
def connect_view(request):
    start_artist = request.params.get('start_artist','Death Grips')
    target_artist = request.params.get('target_artist', 'Kero Kero Bonito')
    print(f'start_artisit={start_artist}, target_artist={target_artist}')

    if(start_artist is None or target_artist is None):
        return Response("Incomplete request.", content_type='text/plain', status=500)

    artist_info=Utils.get_artist_info(start_artist,target_artist)
    print(f'Retrieved artist info {artist_info}')
    
    distance = Utils.better_how_separate(artist_info)
    result = "start_artist={}, target_artist={}. Artists needed using genre metrics {} and furthest depth {}".format(start_artist,target_artist,distance[0],distance[1])
    return Response(result, content_type='text/plain', status=200) 

