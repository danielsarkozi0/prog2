from header import *
import time

class BigPlayer(BoxLayout):
    def __init__(self, **kwargs): 
        super(BigPlayer, self).__init__(**kwargs)
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    def ms_to_mins(self,ms):
        seconds=math.floor((ms/1000)%60)
        minutes=str(math.floor((ms/(1000*60))%60))
        if seconds<10:
            return str( minutes + ':0' + str(seconds) )
        else:
            return str( minutes + ':' + str(seconds) )

    def current_song(self):
        print("what is playing?")
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(access_token)})
        response_json = response.json()
        current_playing_artist_array=[]
        for artist in response_json["item"]["artists"]:
            current_playing_artist_array.append(str(artist["name"])) 
        current_playing_artist = ", ".join(current_playing_artist_array)
        current_playing_title = response_json["item"]["name"]
        current_playing_cover = response_json["item"]["album"]["images"][0]["url"]
        current_playing_duration = self.ms_to_mins((response_json["item"]["duration_ms"]))
        current_playing_progress = self.ms_to_mins((response_json["progress_ms"]))
        current_playing_album = response_json["item"]["album"]["name"]
        self.ids.current_song_name.text=current_playing_title
        self.ids.current_song_artist.text=current_playing_artist
        self.ids.current_track_image.source= str(current_playing_cover)
        self.ids.current_song_length.text=str(current_playing_duration)
        self.ids.current_position.text=str(current_playing_progress)
        self.ids.album_name.text=str(current_playing_album)

    def is_playing(self):
        print("is it playing?")
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(access_token)})
        response_json = response.json()
        return response_json["is_playing"]
    
    def pause_song(self):
        if self.is_playing():
            print("Trying to pause")
            query = "https://api.spotify.com/v1/me/player/pause"
            response = requests.put(query,
                                    headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer {}".format(access_token)})
            self.ids.play_pause_song.source="pics/play_black.png"
        else:
            print("Trying to play")
            query = "https://api.spotify.com/v1/me/player/play"
            response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(access_token)})
            self.ids.play_pause_song.source="pics/pause_black.png"
        self.current_song()

    def next_song(self):
        print("Trying to skip to next")
        query = "https://api.spotify.com/v1/me/player/next"
        response = requests.post(query,
                                headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(access_token)})
        time.sleep(0.3)
        self.current_song()

    def previous_song(self):
        print("Trying to skip to previous")
        query = "https://api.spotify.com/v1/me/player/previous"
        response = requests.post(query,
                                headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(access_token)})

    tmp = 1
    def repeat_song(self):
        print("Repeating....")
        query = "https://api.spotify.com/v1/me/player/repeat"
        if self.tmp % 2 == 0:
            repeat_state = "off"
            self.tmp+=1
            self.ids.repeat_current_song.source="pics/repeat_black.png"
        else:
            repeat_state = "track"
            self.tmp+=1
            self.ids.repeat_current_song.source="pics/repeat_green_track.png"
        print(repeat_state)
        request_body = {"state":repeat_state}
        response = requests.put(query,params=request_body,headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(access_token)})
   
    tmp2 = 1
    def shuffle_song(self):
        print("Shuffling....")
        query = "https://api.spotify.com/v1/me/player/shuffle"
        if self.tmp % 2 == 0:
            repeat_state = False
            self.tmp+=1
            self.ids.shuffle_song.source="pics/shuffle_black.png"
        else:
            repeat_state = True
            self.tmp+=1
            self.ids.shuffle_song.source="pics/shuffle_green.png"
        print(repeat_state)
        request_body = {"state":repeat_state}
        response = requests.put(query,params=request_body,headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(access_token)})