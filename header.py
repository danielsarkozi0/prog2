import kivy
import requests
import json
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label    
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import *
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import math
from secrets import spotify_user_id,spotify_token
from auth import access_token
from bigplayer import BigPlayer
from search import SearchWindow