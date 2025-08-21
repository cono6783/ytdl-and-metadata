import subprocess
import json
import os
import eyed3
from eyed3.id3.frames import ImageFrame
import yt_dlp
import re
import requests
from re import Pattern

from songdata import SongData
import songdata as sd
import playlistparser as playlist






def main():





	ytdl_options = {'allow_playlist_files': False,
	'extract_flat': 'discard_in_playlist',
	'final_ext': 'mp3',
	'format': 'ba[acodec^=mp3]/ba/b',
	'fragment_retries': 10,
	'ignoreerrors': 'only_download',
	'noplaylist': True,
	'outtmpl': {'default': 'progress/%(id)s.%(ext)s', 'pl_thumbnail': ''},
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

	while os.listdir("progress") != []:
		files = os.listdir("progress")
		applyMetadataWithPlaylistData(playlist.repairFromVideo(files[0].split(".")[0]))
		

	
	
	with open("download.txt", "r") as urlfile:
		URLS = urlfile.readlines()

	for url in URLS:
		if playlist.isPlaylist(url):
			print("Autodetected as playlist")
			ytdl_options["writeinfojson"] = False
			ytdl_options["writethumbnail"] = False
			playlistData = playlist.parsePlaylist(url)
			URLS.remove(url)

			with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
				ytdl.download(playlistData.urls)

			applyMetadataWithPlaylistData(playlistData)
		else:
			ytdl_options["writeinfojson"] = True
			ytdl_options["writethumbnail"] = True
			
			with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
				ytdl.download(url)

			applyMetadataWithJSON()
			
			


	with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
		ytdl.download(URLS)

	with open("download.txt", "w") as urlfile:
		urlfile.writelines(URLS)

	



def applyMetadataWithJSON():
	for file in os.listdir("progress"):
		if file.endswith("mp3"): continue
		name = file.split(".")[0]
		with open(f"progress/{name}.info.json", "r") as jsonfile:
			jsondata = json.load(jsonfile)
		
		#Need to do some logic somewhere in here to see if i need to parse the title or not
		
		print()
		#First parse the title
		songData = extract(jsondata["title"])
		if songData == None: return

		#Overwrite b/c if i had to parse the title then the data is not going to be in the json
		songData.overwrite(jsondata)


		print(songData)
		songData.writeDataToFile(f"progress/{name}.mp3")

		os.remove(f"progress/{name}.info.json")

def applyMetadataWithPlaylistData(playlistData : playlist.PlaylistData):

	#Download albumImage first
	response = requests.get(playlistData.albumImage, stream=True) # Not entirely sure if a stream is required
	if response.status_code == 200:
		with open(f"progress/{playlistData.albumName}.jpg", "wb") as imgFile:
			for chunk in response.iter_content(chunk_size=8192):
				imgFile.write(chunk)
		print(f"{playlistData.albumName}.jpg successfully downloaded")
	else:
		print(f"Failed to download image with err code {response.status_code}")



	for file in os.listdir("progress"):
		if playlistData.hasDataFor(file):
			songData = playlistData.generateSongData(file.removesuffix('.mp3'))

			print(songData)

			songData.writeDataToFile(f"progress/{file}")

			audioFile = eyed3.load(f"progress/{file}")
			if audioFile == None:
				print(f"Writing Data failed: Could not find {file}")
				continue

			with open(f"progress/{playlistData.albumName}.jpg", "rb") as imgFile:
				audioFile.tag.images.set(
					ImageFrame.FRONT_COVER,
					imgFile.read(),
					"image/jpeg"
				)
			
			audioFile.tag.save()

			os.rename(f"progress/{file}", f"downloaded/{file}")

	os.remove(f"progress/{playlistData.albumName}.jpg")

			

			





patterns : list[Pattern] = list()

#TODO: write one for the ULTRAKILL stuff by KEYGEN
patterns.append(re.compile(r"\[(?P<genre>.*)\]\s-\s(?P<artist>.*)\s-\s(?P<title>.*)\s\[.*\]")) # Monstercat
patterns.append(re.compile(r"(?P<artist>.*?)\s-\s(?P<title>.*)")) # Standard


def extract(s):
    for pattern in patterns:
        match = pattern.match(s)
        if match != None:
            return sd.fromMatch(match)

    print(f"No match found for {s}")
    return None



if __name__ == "__main__":
	main()
