# coding=UTF-8
class User:
    def __init__(self, guid=None, id=None, password=None):
        self.guid = guid
        self.id = id
        self.password = password


class Voice:
    def __init__(self, guid=None, file_name=None, wav_name=None):
        self.guid = guid
        self.file_name = file_name
        self.wav_name = wav_name
