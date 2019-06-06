import os
from database.database import *
from database.model import Voice
from path import PATH


WEB_URL = 'voice.stevenben.nctu.me'
TTS_TYPE = {
    0: 'mandarin_BZNSYP',
    1: 'english_LJSpeech'
}


def get_voice_url(voice):
    check_voice_type(voice)

    url = os.path.join(WEB_URL, 'static', voice.guid, TTS_TYPE[voice.tts_type], voice.file_name + '.wav')

    return url


def check_voice_name(guid, wav_name):
    voices = select_voices_by_guid(guid)
    print('wav_name =', wav_name)

    if voices:
        for v in voices:
            print('voice wav name =', v.wav_name)
            if wav_name == v.wav_name:
                return False

    return True


def delete_voice(voice):
    try:
        check_voice_type(voice)

        delete_voice_by_filename_and_guid(voice.file_name, voice.guid)

        file_path = os.path.join(PATH['web_static'], voice.guid, TTS_TYPE[voice.tts_type], voice.file_name + '.wav')

        os.system('rm %s' % file_path)
    except Exception as err:
        print('[ERROR - voice] delete voice fail:', err)
        return False

    return True


def check_voice_type(voice):
    if type(voice) != Voice:
        raise TypeError('type must be \'Voice\', but get \'{0}\''.format(type(voice)))
