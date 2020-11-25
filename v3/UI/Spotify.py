# References:
# 1. https://medium.com/@maxtingle/getting-started-with-spotifys-api-spotipy-197c3dc6353b (statistical data)
# 2. https://dev.to/helloiamarra/how-to-play-spotify-songs-and-show-the-album-art-using-spotipy-library-and-python-5eki

import tkinter as tk
import os
import sys
import json
# import spotipy
# import webbrowser
# import spotipy.util as util
# from json.decoder import JSONDecodeError


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class SpotifyView(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.textLabel = tk.Label(
            self,
            fg="green",
            text="Spotify"
        )

