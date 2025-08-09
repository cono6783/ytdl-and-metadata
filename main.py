import subprocess
import json
import os

for file in os.listdir("downloaded"):
    if not file.endswith("mp3"): continue
    name = file.split(".")[0]
    with open(f'downloaded/{name}.info.json', "r") as jsonfile:
        jsondata = json.load(jsonfile)
    print(f'Artist(s): {jsondata["artists"]}')
    print(f'Album: {jsondata["album"]}')
    print(f'Track: {jsondata["track"]}')
    print()

    os.setxattr(f"downloaded/{file}", "artist", jsondata["artists"]) #This exists in linux but not windows :)
    os.setxattr(f"downloaded/{file}", 'album', jsondata['album'])
    os.setxattr(f"downloaded/{file}", 'title', jsondata['track'])




