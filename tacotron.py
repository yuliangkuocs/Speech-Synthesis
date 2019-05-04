##
import os
import pip
from os.path import exists, join, expanduser

os.chdir(expanduser("~"))
wavenet_dir = "wavenet_vocoder"
if not exists(wavenet_dir):
    os.system("git clone https://github.com/r9y9/wavenet_vocoder")

taco2_dir = "Tacotron-2"
if not exists(taco2_dir):
    os.system("git clone https://github.com/r9y9/Tacotron-2")
    os.system("cd Tacotron-2")
    os.system("git checkout -B wavenet3 origin/wavenet3")

##
# ! pip install -q --upgrade "tensorflow<=1.9.0"

# os.chdir(join(expanduser("~"), taco2_dir))
# print(os.getcwd()) # get current os path
# os.system("pip install -q -r requirements.txt")
'''[IMPORT] INSTALLATION PACKAGE (USAGE: pip install [package])
falcon==1.2.0
inflect==0.2.5
librosa==0.5.1 # [IMPORTANT! WATCH HERE!] WIN10 MUST be version==0.5.1 / Ubuntu 16.04 MUST be version==0.6.2 !
matplotlib==2.0.2 # Ben(WIN10) using newer version 3.0.3
numpy==1.13.0 # Ben(WIN10) using newer version 1.16.2
scipy==1.0.0 # Ben(WIN10) using newer version 1.2.1
tqdm==4.11.2 # Ben(WIN10) using newer version 4.31.1
Unidecode==0.4.20'''

# os.chdir(join(expanduser("~"), wavenet_dir))
# os.system("pip install -q -e ".[train]"")
'''[IMPORT] INSTALLATION PACKAGE
1. cd ~/wavenet_vocoder
2. pip install -e ".[train]"
3. For PyTorch, reference this website: https://www.pytorchtutorial.com/pytorch-installation-commands/
4. pip install -e ".[train]"
'''

##
import torch
import tensorflow

print("tensorflow_version=", tensorflow.__version__)

##
os.chdir(join(expanduser("~"), taco2_dir))
if not exists("logs-Tacotron/"):
    os.system("mkdir -p logs-Tacotron")
if not exists("logs-Tacotron/pretrained"):
    os.system("curl -O -L \"https://www.dropbox.com/s/vx7y4qqs732sqgg/pretrained.tar.gz\"")
    os.system("tar xzvf pretrained.tar.gz")
    os.system("mv pretrained logs-Tacotron")

##
os.chdir(join(expanduser("~"), wavenet_dir))
wn_preset = "20180212_multispeaker_cmu_arctic_mixture.json"
wn_checkpoint_path = "20180212_mixture_multispeaker_cmu_arctic_checkpoint_step000740000_ema.pth"
# if not exists(wn_preset):
#   os.system("curl -O -L \"https://www.dropbox.com/s/0vsd7973w20eskz/20180510_mixture_lj_checkpoint_step000320000_ema.json\"")
# if not exists(wn_checkpoint_path):
#   os.system("curl -O -L \"https://www.dropbox.com/s/zdbfprugbagfp2w/20180510_mixture_lj_checkpoint_step000320000_ema.pth\"")


# ##
# os.chdir(join(expanduser("~"), taco2_dir))
#
# %%bash
# cat << EOS > text_list.txt
# This is really awesome!
# This is text-to-speech online demonstration by Tacotron 2 and WaveNet.
# Thanks for your patience.
# EOS
#
# cat text_list.txt
#
# ##
'''Create 'text_list.txt' including the input sentences, moving it to dir 'Tacotron-2' '''
# # Remove old files if exist
# ! rm -rf tacotron_output
# os.system("python synthesize.py --model=Tacotron --mode=eval")
#
# ##
'''pip install IPython'''
import librosa.display
import IPython
from IPython.display import Audio
import numpy as np

# ##
os.chdir(join(expanduser("~"), wavenet_dir))

# Setup WaveNet vocoder hparams
from hparams import hparams

with open(wn_preset) as f:
    hparams.parse_json(f.read())

# Setup WaveNet vocoder
from train import build_model
from synthesis import wavegen

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

model = build_model().to(device)

print("Load checkpoint from {}".format(wn_checkpoint_path))
checkpoint = torch.load(wn_checkpoint_path)
model.load_state_dict(checkpoint["state_dict"])

##
from glob import glob
from tqdm import tqdm

with open("../Tacotron-2/tacotron_output/eval/map.txt") as f:
    maps = f.readlines()
maps = list(map(lambda x: x[:-1].split("|"), maps))
# filter out invalid ones
maps = list(filter(lambda x: len(x) == 2, maps))

print("List of texts to be synthesized")
for idx, (text, _) in enumerate(maps):
    print(idx, text)

##
waveforms = []

for idx, (text, mel) in enumerate(maps):
    print("\n", idx, text)
    mel_path = join("../Tacotron-2", mel)
    c = np.load(mel_path)
    if c.shape[1] != hparams.num_mels:
        np.swapaxes(c, 0, 1)
    # Range [0, 4] was used for training Tacotron2 but WaveNet vocoder assumes [0, 1]
    c = np.interp(c, (0, 4), (0, 1))

    # Generate
    waveform = wavegen(model, c=c, g=6, fast=True, tqdm=tqdm)

    waveforms.append(waveform)

    # Audio
    IPython.display.display(Audio(waveform, rate=hparams.sample_rate))

##
for idx, (text, mel) in enumerate(maps):
    print(idx, text)
    IPython.display.display(Audio(waveforms[idx], rate=hparams.sample_rate))

## Write
from scipy.io.wavfile import write

for i in range(len(waveforms)):
    np.save('wave{}.npy'.format(i), waveforms[i])
    write('output{}.wav'.format(i), 22050, waveforms[i])

## More
pass

pass
