from header import *
import time


class SearchWindow(Screen):
    
    def __init__(self, **kwargs): 
        super(SearchWindow, self).__init__(**kwargs)
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    def search_item_request(self):
        print("searching...")
        search_text = self.ids.search_item.text
        search_text = search_text.replace(" ","%20")
        query = "https://api.spotify.com/v1/search?type=track&q={}".format(search_text)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(access_token)})
        response_json = response.json()
        return response_json
    
    search_counter = 0
    search_item_url_array = []

    def search_item(self):
        self.remove_item()
        time.sleep(0.1)
        response_json = self.search_item_request()
        self.search_counter+=1
        for i in range(20):
            self.search_item_url_array.append(response_json["tracks"]["items"][i]["uri"])

            boxlayout = BoxLayout(orientation="horizontal",size_hint_y=None,height=50)

            card_box_cover = AsyncImage(source=response_json["tracks"]["items"][i]["album"]["images"][2]["url"])

            button = Button(background_color=(83/255,83/255,83/255,1),background_normal="",background_down="",size_hint=(None,None),
                                            height="50dp",width="50dp", on_press=lambda x:self.play_item(self.search_item_url_array[i]), text="PLAY")
            
            boxlayout.add_widget(button)
            boxlayout.add_widget(card_box_cover)


            card_box_title= response_json["tracks"]["items"][i]["name"]

            artists_query_array=[]
            for artist in response_json["tracks"]["items"][i]["artists"]:
                artists_query_array.append(str(artist["name"])) 
            artists_query = ", ".join(artists_query_array)
            card_box_artist = artists_query

            card_box_title_and_artist = Label(text=str(card_box_title+"\n"+card_box_artist),font_size=10)

            boxlayout.add_widget(card_box_title_and_artist)

            self.ids.root_layout.add_widget(boxlayout)

    def remove_item(self):
        if self.search_counter ==0: pass
        else:
            for i in range(20):
                self.ids.root_layout.remove_widget(self.ids.root_layout.children[0])

    def play_item(self,link):
        print("next song...")
        query = "https://api.spotify.com/v1/me/player/queue?uri={}".format(link)
        requests.post(query,
                        headers={"Content-Type": "application/json",
                                    "Authorization": "Bearer {}".format(access_token)})
        BigPlayer().next_song()