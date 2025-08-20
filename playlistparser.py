from selenium import webdriver
from selenium.webdriver.common.by import By

from songdata import SongData

class PlaylistData():
    def __init__(self, artist : str, albumName : str, albumImage : str | None, titles : list[str], urls : list[str], ids : list[str]) -> None:
        self.artist = artist
        self.albumName = albumName
        self.albumImage = "" if albumImage == None else albumImage
        self.titles = titles
        self.urls = urls
        self.ids = ids

    def __str__(self) -> str:
        return f"""Artist: {self.artist}
        Album: {self.albumName}
        Album Image: {self.albumImage}
        Titles: {self.titles}"""




    def hasDataFor(self, idOrFilename : str):
        idOrFilename = idOrFilename.removesuffix(".mp3")
        return idOrFilename in self.ids
    
    def generateSongData(self, id):
        return SongData(title=self.titles[self.ids.index(id)], album=self.albumName, artists=[self.artist], trackNum=self.ids.index(id) + 1)


def isPlaylist(link : str) -> bool:
    return "playlist?list=" in link


def parsePlaylist(link : str) -> PlaylistData:
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=firefox_options)

    driver.get(link)

    driver.implicitly_wait(1)

    artist = driver.find_element(by=By.CSS_SELECTOR, value="ytmusic-responsive-header-renderer").find_element(By.CSS_SELECTOR, "a").text

    albumName = driver.find_element(by=By.CSS_SELECTOR, value="ytmusic-responsive-header-renderer").find_element(by=By.CSS_SELECTOR, value="h1").find_element(by=By.CSS_SELECTOR, value="yt-formatted-string").text

    albumImage = driver.find_element(By.CSS_SELECTOR, "ytmusic-responsive-header-renderer").find_element(By.CLASS_NAME, "thumbnail").find_element(By.CSS_SELECTOR, "img").get_attribute("src")

    ytmrlirs = driver.find_elements(by = By.CSS_SELECTOR, value="ytmusic-responsive-list-item-renderer")

    titles = list()
    urls= list()

    for item in ytmrlirs:
        item_a = item.find_element(by=By.CSS_SELECTOR, value="a")
        titles.append(item_a.text)
        urls.append(item_a.get_attribute("href"))

    ids = list()

    for url in urls:
        ids.append(url.split("watch?v=")[1].split("&list=")[0])

    driver.close()

    return PlaylistData(artist, albumName, albumImage, titles, urls, ids)
        


if __name__ == "__main__":
    pd = parsePlaylist("https://music.youtube.com/playlist?list=OLAK5uy_lzCpGbBL0E2rUrCGFbzZ59QVJoR7vgpTE")
    print(pd)