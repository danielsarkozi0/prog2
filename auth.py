import json
import requests
from secrets import spotify_user_id
from secrets import refresh_token, base_64

class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64
        self.access_token = ""

    def refresh(self):

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": refresh_token},
                                 headers={"Authorization": "Basic " + base_64})

        response_json = response.json()
        print(response_json["access_token"])

        self.access_token = response_json["access_token"]


a = Refresh()
a.refresh()
print("==================================")
print(a.access_token)
access_token = a.access_token