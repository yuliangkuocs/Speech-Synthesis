import os
import numpy as np
from glob import glob
from scipy.io.wavfile import write


DATA_PATH = './WaveData/'
SAMPLE_RATE = 48000

waveDatas = glob(DATA_PATH + '*.npy')


for data in waveDatas:
    outputPath = os.path.dirname(__file__) + 'Result/'
    waveNpData = np.load(data)
    write(outputPath + 'result-{0}.wav'.format(data.replace(DATA_PATH, '').replace('.npy', '')), SAMPLE_RATE, waveNpData)


'''LPCNET trying by Ben on Friday'''
# import os
# import numpy as np
# from glob import glob
# from scipy.io.wavfile import write
#
#
# DATA_PATH = './WaveData/'
# SAMPLE_RATE = 16000
#
# waveDatas = glob(DATA_PATH + '*.npy')
#
#
# for data in waveDatas:
#     outputPath = os.path.dirname(__file__) + '/Result/'
#     waveNpData = np.load(data)
#     waveNpData = waveNpData.reshape((-1,))
#     waveNpData.tofile("mel_220k_0.s16")


