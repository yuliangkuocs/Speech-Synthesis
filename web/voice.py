import os
from database.model import Voice

WEB_URL = 'voice.stevenben.nctu.me'
TTS_TYPE = {
    0: 'mandarin_BZNSYP',
    1: 'english_LJSpeech'
}


def get_voice_url(voice):
    if type(voice) != Voice:
        raise TypeError('[ERROR voice - get_voice_url] type must be \'Voice\', but get \'{0}\''.format(type(voice)))

    url = os.path.join(WEB_URL, 'static', voice.guid, TTS_TYPE[voice.tts_type], voice.file_name + '.wav')

    return url
