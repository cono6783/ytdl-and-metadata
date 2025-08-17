import eyed3


def gen_artist_list(artistList):
    output = ""
    for artist in artistList:
        output += artist + "/"
    return output.removesuffix("/")

class SongData():
    def __init__(self, data) -> None:
        self.title = data["title"] | None
        self.album = data['album'] | None
        self.artists = [data['artists'] | '']
        self.genre = data['genre'] | None

    def overwrite(self, data): # If the right data is not found in data it will not overwrite
        self.title = data["title"] | self.title
        self.album = data['album'] | self.album
        self.artists = [data['artists'] | ''] if self.artists == [''] else self.artists
        self.genre = data['genre'] | self.genre


    def setTitle(self, title : str):
        self.title = title

    def setAlbum(self, album : str):
        self.album = album

    def setArtists(self, artists : list[str]):
        self.artists = artists

    def getTitle(self):
        return self.title
    
    def getAlbum(self):
        return self.album
    
    def getArtistList(self):
        return gen_artist_list(self.artists)
    

    def writeDataToFile(self, file : str):
         
        audioFile = eyed3.load(file)
        audioFile.tag.clear()
        if self.artists[0]:
            audioFile.tag.artist = gen_artist_list(self.artists)
        if self.album:
            audioFile.tag.album = self.album
        if self.title:
            audioFile.tag.title = self.title

        audioFile.tag.save(version=eyed3.id3.ID3_V2_3)


    def __str__(self) -> str:
        output = ""
        if self.artists[0]:
            output += f'Artist(s): {self.artists}\n'
        if self.album:
            output += f'Album: {self.album}\n'
        if self.title:
            output += f'Title: {self.title}\n'
        return output