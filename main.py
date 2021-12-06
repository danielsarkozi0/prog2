from header import *
import time
import schedule

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('myspotify.kv')

class MySpotify(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MySpotify().run()

