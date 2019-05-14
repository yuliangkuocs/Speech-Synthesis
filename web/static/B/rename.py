import os


def int2str(i):
	if i < 10:
		return '00{0}'.format(i)
	elif i < 100:
		return '0{0}'.formate(i)
	else:
		return str(i)


for i in range(int(input('How many wavs you want to rename: '))):
	origin_wav = 'wav-batch_{0}_sentence_000-linear.wav'.format(int2str(i))
	res_wav = 'eval-{0}.wav'.format(int2str(i))

	command = 'mv {0} {1}'.format(origin_wav, res_wav)
	os.system(command)

