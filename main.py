from header import *
import time
import schedule



#Config.set('graphics', 'width', '360')
#Config.set('graphics', 'height', '780')
#360x780

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('myspotify.kv')

class MySpotify(App):
    def build(self):
        return kv

if __name__ == "__main__":
    Window.size = (360, 780)
    MySpotify().run()

