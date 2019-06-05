import os
import time

MODE = ['mandarin_BZNSYP', 'english_LJSpeech']
PATH = {
    'mandarin_BZNSYP': '/home/steven/Desktop/TTS-Mandarin',
    'english_LJSpeech': '',
    'web_static': '/home/steven/Desktop/Speech-Synthesis/web/static'
}

TIMEOUT = 30


def tts(guid, text, file_name, mode):
    check_mode(mode)

    dir_now = os.path.abspath(os.path.curdir)

    os.chdir(PATH[mode])

    write_text(guid, text)

    os.system('./run.sh')

    is_timeout = True

    if check_synthesis(guid):
        file_dir_path = os.path.join(PATH['web_static'], guid, mode)

        os.system('mkdir -p {0}'.format(file_dir_path))
        os.system('cp result/{0}.wav {1}'.format(guid, file_dir_path + '/' + file_name + '.wav'))
        os.system('rm result/{0}.wav'.format(guid))

    else:
        is_timeout = False

    os.chdir(dir_now)

    if not is_timeout:
        raise TimeoutError('[ERROR - TTS] synthesis timeout')

    return True


def check_mode(mode):
    if mode not in MODE:
        raise KeyError('Can not find the mode \'%s\'' % mode)


def write_text(guid, text):
    file_text = open('text/{0}.txt'.format(guid), 'w', encoding='UTF-8')
    file_text.write(text)
    file_text.close()


def check_synthesis(guid):
    start = time.time()

    while time.time() - start < TIMEOUT:
        time.sleep(1)

        if os.path.exists('result/{0}.wav'.format(guid)):
            return True

    return False
