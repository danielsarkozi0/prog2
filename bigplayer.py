from header import *
import time
import schedule
import threading

class BigPlayer(Screen):
    def __init__(self, **kwargs):
        super(BigPlayer, self).__init__(**kwargs)
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        t = threading.Thread(target=self.ScheduleCurrently)
        t.daemon = True
        t.start()

    def ScheduleCurrently(self):
        schedule.every(2).seconds.do(self.current_song)
        while True:
            schedule.run_pending()

    def ms_to_mins(self,ms):
        seconds=math.floor((ms/1000)%60)
        minutes=str(math.floor((ms/(1000*60))%60))
        if seconds<10:
            return str( minutes + ':0' + str(seconds) )
        else:
            return str( minutes + ':' + str(seconds) )

    def ms_to_sec(self,ms):
        seconds=math.floor((ms/1000))
        return seconds

    def progress(self,progress,duration):
        dur_max = self.ms_to_sec(duration)
        prog_value = self.ms_to_sec(progress)
        self.ids.progressbar_song.max = dur_max
        self.ids.progressbar_song.value = prog_value

    def current_song(self):
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
        self.progress((response_json["progress_ms"]),(response_json["item"]["duration_ms"]))

    def is_playing(self):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(access_token)})
        response_json = response.json()
        return response_json["is_playing"]

    def pause_song(self):
        if self.is_playing():
            query = "https://api.spotify.com/v1/me/player/pause"
            response = requests.put(query,
                                    headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer {}".format(access_token)})
            self.ids.play_pause_song.source="pics/play_black.png"
        else:
            query = "https://api.spotify.com/v1/me/player/play"
            response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(access_token)})
            self.ids.play_pause_song.source="pics/pause_black.png"
        self.current_song()

    def next_song(self):
        query = "https://api.spotify.com/v1/me/player/next"
        response = requests.post(query,
                                headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(access_token)})
        time.sleep(0.3)
        self.current_song()

    def previous_song(self):
        query = "https://api.spotify.com/v1/me/player/previous"
        response = requests.post(query,
                                headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(access_token)})

    repeat_song_counter = 1
    def repeat_song(self):
        query = "https://api.spotify.com/v1/me/player/repeat"
        if self.repeat_song_counter % 2 == 0:
            repeat_state = "off"
            self.repeat_song_counter+=1
            self.ids.repeat_current_song.source="pics/repeat_black.png"
        else:
            repeat_state = "track"
            self.repeat_song_counter+=1
            self.ids.repeat_current_song.source="pics/repeat_green_track.png"
        request_body = {"state":repeat_state}
        response = requests.put(query,params=request_body,headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(access_token)})

    shuffle_song_counter = 1
    def shuffle_song(self):
        query = "https://api.spotify.com/v1/me/player/shuffle"
        if self.shuffle_song_counter % 2 == 0:
            repeat_state = False
            self.shuffle_song_counter+=1
            self.ids.shuffle_song.source="pics/shuffle_black.png"
        else:
            repeat_state = True
            self.shuffle_song_counter+=1
            self.ids.shuffle_song.source="pics/shuffle_green.png"
        request_body = {"state":repeat_state}
        response = requests.put(query,params=request_body,headers={"Content-Type": "application/json",
                                "Authorization": "Bearer {}".format(access_token)})
