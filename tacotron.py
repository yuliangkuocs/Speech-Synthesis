import os
import numpy as np
import torch
import tensorflow
from tqdm import tqdm
from argparse import ArgumentParser


NOW_DIR = os.path.dirname(__file__)
WAVENET_DIR = 'Wavenet'
TACOTRON_DIR = 'Tacotron'

parser = ArgumentParser()
parser.add_argument('--text_list', default=None, dest='text_list', help='Use the your txt file to import your text')

args = parser.parse_args()


def isPathExist(path):
    return os.path.exists(path)


def runTacotron():
    os.chdir(os.path.join(NOW_DIR, TACOTRON_DIR))

    command = 'python synthesize.py --model=Tacotron --mode=eval --text_list={0}'.format('../' + args.text_list)

    os.system(command)


def runWavenet():
    os.chdir(os.path.join(NOW_DIR, WAVENET_DIR))

    wavenetCheckpoint = ''
    wavenetPreset = ''

    from hparams import hparams
    from train import build_model
    from synthesis import wavegen

    with open(wavenetPreset) as f:
        hparams.parse_json(f.read())

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    model = build_model().to(device)

    print("Load checkpoint from {}".format(wavenetCheckpoint))
    checkpoint = torch.load(wavenetCheckpoint)
    model.load_state_dict(checkpoint["state_dict"])

    with open("../Tacotron/tacotron_output/eval/map.txt") as f:
        maps = f.readlines()
    maps = list(map(lambda x: x[:-1].split("|"), maps))
    # filter out invalid ones
    maps = list(filter(lambda x: len(x) == 2, maps))

    print("List of texts to be synthesized")
    for idx, (text, _) in enumerate(maps):
        print(idx, text)

    waveforms = []

    for idx, (text, mel) in enumerate(maps):
        print("\n", idx, text)
        mel_path = os.path.join("../Tacotron", mel)
        c = np.load(mel_path)
        if c.shape[1] != hparams.num_mels:
            np.swapaxes(c, 0, 1)

        # Range [0, 4] was used for training Tacotron but WaveNet vocoder assumes [0, 1]
        c = np.interp(c, (0, 4), (0, 1))

        # Generate
        waveform = wavegen(model, c=c, g=6, fast=True, tqdm=tqdm)

        waveforms.append(waveform)

    for idx, (text, mel) in enumerate(maps):
        print(idx, text)


if __name__ == '__main__':
    print("tensorflow_version=", tensorflow.__version__)

    runTacotron()
    runWavenet()


