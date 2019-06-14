# coding=UTF-8
class User:
    def __init__(self, guid=None, id=None, password=None):
        self.guid = guid
        self.id = id
        self.password = password


class Voice:
    def __init__(self, guid=None, file_name=None, wav_name=None, tts_type=None):
        self.guid = guid
        self.file_name = file_name
        self.wav_name = wav_name
        self.tts_type = tts_type


class UserTest:
    def __init__(self, en_itri=None, en_ljspeech=None, en_milabs=None, ch_google=None, ch_mandarin=None):
        self.en_itri = en_itri
        self.en_ljspeech = en_ljspeech
        self.en_milabs = en_milabs
        self.ch_google = ch_google
        self.ch_mandarin = ch_mandarin
