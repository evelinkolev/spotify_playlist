import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://billboard.com/charts/hot-100/{date}/")
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
song_names_headers = soup.find_all(name="h3", class_="a-no-trucate")
song_names = [title.getText().strip() for title in song_names_headers]
#print(song_names)

#feed your credential eg-> YOUR_APP_CLIENT_ID= "XXXXXXXXXXXXXX"
YOUR_APP_CLIENT_ID = ""
YOUR_APP_CLIENT_SECRET = ""
YOUR_APP_REDIRECT_URI = "http://example.com"

#now creating playlist in spotify

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=YOUR_APP_CLIENT_ID,
        client_secret=YOUR_APP_CLIENT_SECRET,
        redirect_uri=YOUR_APP_REDIRECT_URI,
        scope="playlist-modify-private",
        cache_path="token.txt",
))

results = sp.current_user()
USER_ID = results['id']
#print(f"USER_ID is {USER_ID}")

song_uris = [sp.search(title)['tracks']['items'][0]['uri'] for title in song_names]

PLAYLIST_ID = sp.user_playlist_create(user=USER_ID, public=False, name=f"{date} BillBoard-100")['id']

sp.playlist_add_items(playlist_id=PLAYLIST_ID, items=song_uris)