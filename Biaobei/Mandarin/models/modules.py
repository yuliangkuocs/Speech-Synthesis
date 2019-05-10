import tensorflow as tf
from tensorflow.contrib.rnn import GRUCell


def prenet(inputs, is_training, layer_sizes, scope=None):
  x = inputs
  drop_rate = 0.5 if is_training else 0.0
  with tf.variable_scope(scope or 'prenet'):
    for i, size in enumerate(layer_sizes):
      dense = tf.layers.dense(x, units=size, activation=tf.nn.relu, name='dense_%d' % (i+1))
      x = tf.layers.dropout(dense, rate=drop_rate, training=is_training, name='dropout_%d' % (i+1))
  return x


def encoder_cbhg(inputs, input_lengths, is_training, depth):
  input_channels = inputs.get_shape()[2]
  return cbhg(
    inputs,
    input_lengths,
    is_training,
    scope='encoder_cbhg',
    K=16,
    projections=[128, input_channels],
    depth=depth)


def post_cbhg(inputs, input_dim, is_training, depth):
  return cbhg(
    inputs,
    None,
    is_training,
    scope='post_cbhg',
    K=8,
    projections=[256, input_dim],
    depth=depth)


def cbhg(inputs, input_lengths, is_training, scope, K, projections, depth):
  with tf.variable_scope(scope):
    with tf.variable_scope('conv_bank'):
      # Convolution bank: concatenate on the last axis to stack channels from all convolutions
      conv_outputs = tf.concat(
        [conv1d(inputs, k, 128, tf.nn.relu, is_training, 'conv1d_%d' % k) for k in range(1, K+1)],
        axis=-1
      )

    # Maxpooling:
    maxpool_output = tf.layers.max_pooling1d(
      conv_outputs,
      pool_size=2,
      strides=1,
      padding='same')

    # Two projection layers:
    proj1_output = conv1d(maxpool_output, 3, projections[0], tf.nn.relu, is_training, 'proj_1')
    proj2_output = conv1d(proj1_output, 3, projections[1], lambda _:_, is_training, 'proj_2')

    # Residual connection:
    highway_input = proj2_output + inputs

    half_depth = depth // 2
    assert half_depth*2 == depth, 'encoder and postnet depths must be even.'

    # Handle dimensionality mismatch:
    if highway_input.shape[2] != half_depth:
      highway_input = tf.layers.dense(highway_input, half_depth)

    # 4-layer HighwayNet:
    for i in range(4):
      highway_input = highwaynet(highway_input, 'highway_%d' % (i+1), half_depth)
    rnn_input = highway_input

    # Bidirectional RNN
    outputs, states = tf.nn.bidirectional_dynamic_rnn(
      ZoneoutLSTMCell(half_depth, is_training, zoneout_factor_cell=0.1, zoneout_factor_output=0.1),
      ZoneoutLSTMCell(half_depth, is_training, zoneout_factor_cell=0.1, zoneout_factor_output=0.1),
      # GRUCell(half_depth),
      # GRUCell(half_depth),
      rnn_input,
      sequence_length=input_lengths,
      dtype=tf.float32)
    return tf.concat(outputs, axis=2)  # Concat forward and backward


def highwaynet(inputs, scope, depth):
  with tf.variable_scope(scope):
    H = tf.layers.dense(
      inputs,
      units=depth,
      activation=tf.nn.relu,
      name='H')
    T = tf.layers.dense(
      inputs,
      units=depth,
      activation=tf.nn.sigmoid,
      name='T',
      bias_initializer=tf.constant_initializer(-1.0))
    return H * T + inputs * (1.0 - T)


def conv1d(inputs, kernel_size, channels, activation, is_training, scope):
  with tf.variable_scope(scope):
    conv1d_output = tf.layers.conv1d(
      inputs,
      filters=channels,
      kernel_size=kernel_size,
      activation=None,
      padding='same')
    batched = tf.layers.batch_normalization(conv1d_output, training=is_training)
    return activation(batched)


class ZoneoutLSTMCell(tf.nn.rnn_cell.RNNCell):
  '''Wrapper for tf LSTM to create Zoneout LSTM Cell

  inspired by:
  https://github.com/teganmaharaj/zoneout/blob/master/zoneout_tensorflow.py

  Published by one of 'https://arxiv.org/pdf/1606.01305.pdf' paper writers.

  Many thanks to @Ondal90 for pointing this out. You sir are a hero!
  '''
  def __init__(self, num_units, is_training, zoneout_factor_cell=0., zoneout_factor_output=0., state_is_tuple=True, name=None):
    '''Initializer with possibility to set different zoneout values for cell/hidden states.
    '''
    zm = min(zoneout_factor_output, zoneout_factor_cell)
    zs = max(zoneout_factor_output, zoneout_factor_cell)

    if zm < 0. or zs > 1.:
      raise ValueError('One/both provided Zoneout factors are not in [0, 1]')

    self._cell = tf.nn.rnn_cell.LSTMCell(num_units, state_is_tuple=state_is_tuple, name=name)
    self._zoneout_cell = zoneout_factor_cell
    self._zoneout_outputs = zoneout_factor_output
    self.is_training = is_training
    self.state_is_tuple = state_is_tuple

  @property
  def state_size(self):
    return self._cell.state_size

  @property
  def output_size(self):
    return self._cell.output_size

  def __call__(self, inputs, state, scope=None):
    '''Runs vanilla LSTM Cell and applies zoneout.
    '''
    #Apply vanilla LSTM
    output, new_state = self._cell(inputs, state, scope)

    if self.state_is_tuple:
      (prev_c, prev_h) = state
      (new_c, new_h) = new_state
    else:
      num_proj = self._cell._num_units if self._cell._num_proj is None else self._cell._num_proj
      prev_c = tf.slice(state, [0, 0], [-1, self._cell._num_units])
      prev_h = tf.slice(state, [0, self._cell._num_units], [-1, num_proj])
      new_c = tf.slice(new_state, [0, 0], [-1, self._cell._num_units])
      new_h = tf.slice(new_state, [0, self._cell._num_units], [-1, num_proj])

    #Apply zoneout
    if self.is_training:
      #nn.dropout takes keep_prob (probability to keep activations) not drop_prob (probability to mask activations)!
      c = (1 - self._zoneout_cell) * tf.nn.dropout(new_c - prev_c, (1 - self._zoneout_cell)) + prev_c
      h = (1 - self._zoneout_outputs) * tf.nn.dropout(new_h - prev_h, (1 - self._zoneout_outputs)) + prev_h
    else:
      c = (1 - self._zoneout_cell) * new_c + self._zoneout_cell * prev_c
      h = (1 - self._zoneout_outputs) * new_h + self._zoneout_outputs * prev_h

    new_state = tf.nn.rnn_cell.LSTMStateTuple(c, h) if self.state_is_tuple else tf.concat(1, [c, h])

    return output, new_state
