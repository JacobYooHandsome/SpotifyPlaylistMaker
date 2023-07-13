from bs4 import BeautifulSoup
import requests
import spotify_auth
from pprint import pprint

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}").text

soup = BeautifulSoup(response, "html.parser")

titles = [item.getText().strip() for item in soup.find_all(name="h3", class_="a-no-trucate")]

spotify_auth.refresh_token()

headers = {
    'Authorization': f'Bearer {spotify_auth.access_token}'
}

sp_playlist_params = {
    "name":f"The top billboard for: {date}",
}

sp_playlist = requests.post("https://api.spotify.com/v1/users/cm3ap7l18qsa4jd922fyszfsz/playlists", json=sp_playlist_params, headers=headers)
playlist_id = sp_playlist.json()['id']

id_list = []

for title in titles:
    search_params = {
        "q": f"year:{date[:4]} track:{title}",
        "type":"track",
        "limit": 1,
    }
    response = requests.get('https://api.spotify.com/v1/search', params=search_params, headers=headers)
    result = response.json()
    try:
        result_id = "spotify:track:" + result['tracks']['items'][0]['id']
    except:
        result_id = title
    else:
        id_list.append(result_id)

pprint(id_list)

playlist_params = {
    "uris": id_list
}

response = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json=playlist_params)
print(response.json())
