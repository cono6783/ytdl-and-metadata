import subprocess
import json
import os
import eyed3
import yt_dlp
import re
from re import Pattern

from songdata import SongData






def main():



	ytdl_options = {'allow_playlist_files': False,
	'extract_flat': 'discard_in_playlist',
	'final_ext': 'mp3',
	'format': 'ba[acodec^=mp3]/ba/b',
	'fragment_retries': 10,
	'ignoreerrors': 'only_download',
	'noplaylist': True,
	'outtmpl': {'default': 'downloaded/%(id)s.%(ext)s', 'pl_thumbnail': ''},
	'postprocessors': [{'key': 'FFmpegExtractAudio',
		'nopostoverwrites': False,
		'preferredcodec': 'mp3',
		'preferredquality': '5'},
		{'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
		{'key': 'FFmpegConcat',
		'only_multi_video': True,
		'when': 'playlist'}],
	'retries': 10,
	'writeinfojson': True,
	'writethumbnail': True}
	
	with open("download.txt", "r") as urlfile:
		URLS = urlfile.readlines()
	with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
		ytdl.download(URLS)

	for file in os.listdir("downloaded"):
		if file.endswith("mp3"): continue
		name = file.split(".")[0]
		with open(f"downloaded/{name}.info.json", "r") as jsonfile:
			jsondata = json.load(jsonfile)
		
		#Need to do some logic somewhere in here to see if i need to parse the title or not
		
		print()
		#First parse the title
		songData = SongData(extract(jsondata["title"]))

		#Overwrite b/c if i had to parse the title then the data is not going to be in the json
		songData.overwrite(jsondata)


		print(songData)
		songData.writeDataToFile(f"downloaded/{name}.mp3")

		os.remove(f"downloaded/{name}.info.json")




patterns : list[Pattern] = list()

#TODO: write one for the ULTRAKILL stuff by KEYGEN
patterns.append(re.compile(r"\[(?P<genre>.*)\]\s-\s(?P<artist>.*)\s-\s(?P<title>.*)\s\[.*\]")) # Monstercat
patterns.append(re.compile(r"(?P<artist>.*?)\s-\s(?P<title>.*)")) # Standard


def extract(s):
    for pattern in patterns:
        match = pattern.match(s)
        if match != None:
            return SongData(match)

    print(f"No match found for {s}")
    return None



if __name__ == "__main__":
	main()
