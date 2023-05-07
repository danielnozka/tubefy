from datetime import datetime


class Song:

    def __init__(self, id_: str, title: str, artist: str, creation_date: datetime, file: str):

        self.id = id_
        self.title = title
        self.artist = artist
        self.creation_date = creation_date
        self.file = file
