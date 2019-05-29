# To transform USAPolitician dataset into LJSpeech-like form (to generate 'metadata.csv')
# After run this program, we can run preprocess.py just like LJSpeech

import argparse
import csv
import os


def csv_generate(args):
    if not args.dataset:
        raise ValueError('Please Enter an USA politician Dataset!!')
    else:
        USA_dir = os.path.join('DATA/USA_Politician/data', args.dataset, 'data/')
        txt_dir = os.path.join(USA_dir, 'txt/', args.dataset)

        features = []
        for files in os.listdir(txt_dir):
            with open(os.path.join(txt_dir, files), 'r', encoding='utf-8') as txt:
                transcript = txt.readlines()
                if len(transcript) != 0 :
                    features.append([files.split('.')[0], transcript[0]])
        with open(os.path.join(USA_dir, 'metadata.csv'), 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for i in range(len(features)):
                # repeat of '|' + features[i][1] is just because LJSpeech-like
                row = [features[i][0] + '|' + features[i][1] + '|' + features[i][1]]
                writer.writerow(row)
            csv_file.close()

        print('Finish generating metadata.csv for ', args.dataset)


def main():
    print('initializing USAPolitician_preprocessing..')
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default=False, help='[bill-clinton, donald-trump, hillary-clinton, obama]')
    args = parser.parse_args()

    csv_generate(args)


if __name__ == '__main__':
    main()
