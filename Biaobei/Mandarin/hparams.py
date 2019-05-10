import tensorflow as tf


# Default hyperparameters:
hparams = tf.contrib.training.HParams(
  # Comma-separated list of cleaners to run on text prior to training and eval. For non-English
  # text, you may want to use "basic_cleaners" or "transliteration_cleaners" See TRAINING_DATA.md.
  cleaners='basic_cleaners',

  # Audio:
  fft_size=2048,
  n_f0=1,
  n_mgc=60,
  n_ap=5,
  mcep_alpha=0.77, #0.58(16k) 0.65(22050) 0.76(44100)
  sample_rate=48000,
  max_frame_num=1600,
  frame_shift_ms=5.5,

  # Model:
  outputs_per_step=2,
  embed_depth=512,
  prenet_depths=[256, 256],
  encoder_depth=256,
  postnet_depth=512,
  attention_depth=128,
  decoder_depth=1024,

  # Training:
  batch_size=32,
  adam_beta1=0.9,
  adam_beta2=0.999,
  initial_learning_rate=0.001,
  decay_learning_rate=True,
  use_cmudict=False,  # Use CMUDict during training to learn pronunciation of ARPAbet phonemes

  # Eval:
  max_iters=1000,
)


def hparams_debug_string():
  values = hparams.values()
  hp = ['  %s: %s' % (name, values[name]) for name in sorted(values)]
  return 'Hyperparameters:\n' + '\n'.join(hp)
