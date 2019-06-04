import os


def tts(guid, text, mode='mandarin'):
    dir_now = os.path.abspath(os.path.curdir)

    if mode == 'mandarin':
        os.chdir('/home/steven/Desktop/TTS-Mandarin')

        file_text = open('text/{0}.txt'.format(guid), 'w', encoding='UTF-8')
        file_text.write(text)
        file_text.close()

        os.system('./run.sh')

        while True:
            isFinish = os.path.exists('result/{0}.wav'.format(guid))
            if isFinish:
                break

        static_path = '/home/steven/Desktop/Speech-Synthesis/web/static/'
        os.system('cp result/{0}.wav {1}{0}.wav'.format(guid, static_path))

        os.chdir(dir_now)
        return True

    return False
