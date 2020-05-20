import spotipy
import spotipy.util as util
import json
from datetime import datetime
from random import random
import variables as v

def find_today_episode(date, podcastName):
    searchResults = spotifyObject.search(podcastName,50,0,"episode")
    while True:
        for result in searchResults['episodes']['items']:
            try:
                if(result["release_date"] == date):
                    #print(json.dumps(result, sort_keys=True, indent=4))
                    return result["uri"]
            except TypeError:
                continue
        if(searchResults['episodes']['next'] != None):
            searchResults = spotifyObject.next(searchResults['episodes'])
        else: 
            print ("Error: Today's episode not found")

def random_music(date):
    searchResults = spotifyObject.current_user_playlists()
    print(searchResults)
    for result in searchResults["items"]:
        if(result["name"] == v.playlistName):
            randomNumber = (random() * 100) % 80
            tracks = spotifyObject.playlist_tracks(result["id"])
            return tracks["items"][int(randomNumber)]["track"]["uri"]


    
username = v.username
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
podcastNames = [v.podcastName1, v.podcastName2]

token = util.prompt_for_user_token(username,
                        scope,
                        client_id= v.client_id,
                        client_secret= v.client_secret,
                        redirect_uri= v.redirect_uri
                        )

spotifyObject = spotipy.Spotify(auth=token)
deviceID = spotifyObject.devices()['devices'][0]["id"]
date = str(datetime.date(datetime.now()))

uriList = []
uri = random_music(date)
uriList.append(uri)


for name in podcastNames:
    uri = find_today_episode(date,name)
    uriList.append(uri)

spotifyObject.start_playback(device_id = deviceID , uris = uriList)
#spotifyObject.add_to_queue(,deviceID)