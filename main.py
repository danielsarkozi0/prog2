from header import *

#Config.set('graphics', 'width', '360')
#Config.set('graphics', 'height', '780')
#360x780
class MySpotify(App):
    def build(self):
        #return bigplayer.BigPlayer()
        return search.SearchWindow()

if __name__ == "__main__":
    Window.size = (360, 780)
    MySpotify().run()