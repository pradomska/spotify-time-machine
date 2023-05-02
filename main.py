from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
APP_REDIRECT_URI = "http://example.com"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

billboard_endpoint = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(billboard_endpoint)
response.encoding = "UTF-8"
web_text = response.text
soup = BeautifulSoup(web_text, "html.parser")
# print(soup.prettify())

titles = [title.getText().strip("\t\n") for title in soup.select("li ul li h3")]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=APP_REDIRECT_URI,
                                               scope="playlist-modify-private"))
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
