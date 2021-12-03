from header import *

class SearchWindow(GridLayout):
    
    def __init__(self, **kwargs): 
        super(SearchWindow, self).__init__(**kwargs)

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

    def search_item(self):
        response_json = self.search_item_request()
        for i in range(20):
            boxlayout = BoxLayout(orientation="horizontal",size_hint_y=None,height=50)

            card_box_cover = AsyncImage(source=response_json["tracks"]["items"][i]["album"]["images"][2]["url"])
            boxlayout.add_widget(card_box_cover)

            card_box_title= Label(text=response_json["tracks"]["items"][i]["name"])
            boxlayout.add_widget(card_box_title)

            artists_query_array=[]
            for artist in response_json["tracks"]["items"][i]["artists"]:
                artists_query_array.append(str(artist["name"])) 
            artists_query = ", ".join(artists_query_array)
            card_box_artist = Label(text=artists_query)
            boxlayout.add_widget(card_box_artist)
            self.ids.root_layout.add_widget(boxlayout)
