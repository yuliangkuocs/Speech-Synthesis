from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
import glob
from hparams import hparams as hp
from util import audio


def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):
  '''Preprocesses the THCHS30 dataset from a given input path into a given output directory.

    Args:
      in_dir: The directory where you have downloaded the THCHS30 dataset
      out_dir: The directory to write the output into
      num_workers: Optional number of worker processes to parallelize across
      tqdm: You can optionally pass tqdm to get a nice progress bar

    Returns:
      A list of tuples describing the training examples. This should be written to train.txt
  '''

  # We use ProcessPoolExecutor to parallize across processes. This is just an optimization and you
  # can omit it and just call _process_utterance on each input if you want.
  executor = ProcessPoolExecutor(max_workers=num_workers)
  futures = []
  index = 1

  trn_files = glob.glob(os.path.join(in_dir, 'biaobei_48000', '*.trn'))

  for trn in trn_files:
    with open(trn) as f:
      pinyin = f.readline().strip('\n')
      wav_file = trn[:-4] + '.wav'
      task = partial(_process_utterance, out_dir, index, wav_file, pinyin)
      futures.append(executor.submit(task))
      index += 1
  return [future.result() for future in tqdm(futures) if future.result() is not None]


def _process_utterance(out_dir, index, wav_path, pinyin):
  '''Preprocesses a single utterance audio/text pair.

  This writes the mel and linear scale spectrograms to disk and returns a tuple to write
  to the train.txt file.

  Args:
    out_dir: The directory to write the spectrograms into
    index: The numeric index to use in the spectrogram filenames.
    wav_path: Path to the audio file containing the speech input
    pinyin: The pinyin of Chinese spoken in the input audio file

  Returns:
    A (spectrogram_filename, mel_filename, n_frames, text) tuple to write to train.txt
  '''

  # Load the audio to a numpy array:
  wav = audio.load_wav(wav_path)

  # trim silence
  wav = audio.trim_silence(wav)

  # feature extraction
  f0, sp, ap = audio.feature_extract(wav)
  n_frames = len(f0)
  if n_frames > hp.max_frame_num:
    return None

  # feature normalization
  lf0 = audio.f0_normalize(f0)
  mgc = audio.sp_normalize(sp)
  bap = audio.ap_normalize(ap)

  lf0_file = 'lf0-%05d.npy' % index
  mgc_file = 'mgc-%05d.npy' % index
  bap_file = 'bap-%05d.npy' % index
  np.save(os.path.join(out_dir, lf0_file), lf0, allow_pickle=False)
  np.save(os.path.join(out_dir, mgc_file), mgc, allow_pickle=False)
  np.save(os.path.join(out_dir, bap_file), bap, allow_pickle=False)

  # Return a tuple describing this training example:
  return (lf0_file, mgc_file, bap_file, n_frames, pinyin)
