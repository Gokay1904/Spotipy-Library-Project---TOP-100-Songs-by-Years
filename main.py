from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re


#You have to first obtain your client_id and client_secret using spotify api
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="YOUR CLIENT ID", #Put your id here
        client_secret="YOUR CLIENT SECRET", #Put your client secret here
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

#Input your date for searching top100 songs by years.
date = input("Please enter the date you wanted in that format: YYYY-MM-DD \n")

year= date.split("-")[0]

#This is the website where the top100 song is scraped
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
soup = BeautifulSoup(response.text,'html.parser')

#Scraping proccess
songs = []
song_names_spans = soup.select(selector="li ul li h3", id_= "title-of-a-story")
song_names = [song.getText() for song in song_names_spans]


for song in song_names:

    songNew = re.sub(r'\t', '', song)
    songNew = re.sub(r'\n', '', songNew)


    song_names[song_names.index(song)] = songNew

#For debugging
print(song_names)

song_uris = []

#For automated list creation.
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
for song in song_names:

    result = sp.search(q=f"track:{song} year:{year}", type= "track")
    #We are checking if the realated song was found.
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Finally add the songs into our spotify list automatically.
sp.playlist_add_items(playlist_id=playlist["id"],items = song_uris)
