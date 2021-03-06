#!/usr/bin/env python

import requests
import json
import shutil
import traceback

token = "ENTER_VALID_TOKEN" # https://developer.spotify.com/console/get-browse-categories/
headers={"Content-Type":"application/json","Authorization":"Bearer %s"%token,"Accept":"application/json"}

response=json.loads(requests.get("https://api.spotify.com/v1/browse/categories", headers=headers).content)

# GET ALL CATEGORIES AVAILABLE BY SPOTIFY
for item in response["categories"]["items"]:
    #GET THE PLAYLISTS AVAILABLE WITHIN EACH CATEGORY
    r=json.loads(requests.get(item["href"]+"/playlists?limit=50",headers=headers).content)

    try:
        for item in r["playlists"]["items"]:
            # GET THE TRACKS WITHIN EACH PLAYLIST
            r_2=json.loads(requests.get(item["href"]+"/tracks?limit=100",headers=headers).content)
            for item in r_2["items"]:
                try:
                    # FOR EACH TRACK IN THE PLAYLIST CHECK IF THERE IS A PREVIEW AVAILABLE
                    if(item["track"]["preview_url"]!=None):
                        track_id=item["track"]["id"]
                        album_id=item["track"]["album"]["id"]
                        # WE SAVE THE AUDIO ANALYSIS BY SPOTIFY, ALBUM INFORMATION, AUDIO FEATURES GENERATED BY SPOTIFY, 30 SECOND PREVIEW AND THE ALBUM COVER
                        audio_analysis=json.loads(requests.get("https://api.spotify.com/v1/audio-analysis/%s"%track_id,headers=headers).content)
                        album_information=json.loads(requests.get("https://api.spotify.com/v1/albums/%s"%album_id,headers=headers).content)
                        audio_features=json.loads(requests.get("https://api.spotify.com/v1/audio-features/%s"%track_id,headers=headers).content)
                        with open('album_information/%s.json'%track_id, 'w') as outfile:
                            json.dump(album_information, outfile)
                        with open('audio_analysis/%s.json'%track_id, 'w') as outfile:
                            json.dump(audio_analysis, outfile)
                        with open('audio_features/%s.json'%track_id, 'w') as outfile:
                            json.dump(audio_features, outfile)
                        image_url=item["track"]["album"]["images"][0]["url"]
                        r_image = requests.get(image_url, stream=True)
                        with open("images/%s.jpeg"%track_id, 'wb') as f:
                            r_image.raw.decode_content = True
                            shutil.copyfileobj(r_image.raw, f)
                        item["track"]["preview_url"]
                        mp3 = requests.get(item["track"]["preview_url"])
                        with open("audio/%s.mp3"%track_id, 'wb') as f:
                            f.write(mp3.content)
                except Exception as e:
                    traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
