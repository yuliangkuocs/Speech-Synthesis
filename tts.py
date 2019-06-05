'''
Architecture:
    text/
    voices/
    Tacotron/
    result/
    tts.py
'''
import os
from glob import glob

def set_sentence():
    file_paths = glob('text/*.txt')
    guids = []

    for file_path in file_paths:
        guid = file_path.replace('text/', '').replace('.txt', '')
        guids.append(guid)

    return guids


def set_voice(user_choice):
    # ckpt steps, respectively
    voices = {'ljspeech', 
            'mary_ann(M-AILABS)', 
            'elliot_miller(M-AILABS)', 
            'noTune_obama', 
            'hillary_clinton'}
    
    # Reset checkpoint
    os.system('rm Tacotron/logs-Tacotron-2/taco_pretrained/checkpoint')
    os.system('cp voices/{0}/checkpoint Tacotron/logs-Tacotron-2/taco_pretrained/'.format(user_choice))
    # Copy hparams
    os.system('rm Tacotron/hparams.py')
    os.system('cp voices/{0}/hparams.py Tacotron/'.format(user_choice))


if __name__ == '__main__':
    guids = set_sentence()
    print(guids)
    voice = 'mary_ann\(M-AILABS\)' # Need received from WEB
    set_voice(voice)
    
    dir_now = os.path.abspath(os.path.curdir)
    os.chdir(dir_now + '/Tacotron')

    for guid in guids:
        os.system('python synthesize.py --text_list=../text/{0}.txt'.format(guid))
        os.system('cp tacotron_output/logs-eval/wavs/wav-batch_0_sentence_0-linear.wav ../result/{0}.wav'.format(guid))
        os.system('rm ../text/{0}.txt'.format(guid))
