import matplotlib.pyplot as plt
from database.database import *
from database.model import UserTest
from path import PATH


def insert_test_score(request_data):
    user_test = UserTest(request_data['en_google'], request_data['en_ljspeech'], request_data['en_milabs'],
                         request_data['ch_google'], request_data['ch_mandarin'])

    is_insert = insert_user_test(user_test)

    if not is_insert:
        raise IndexError('insert user test fail')

    all_user_tests = select_user_tests()
    avg_scores = get_avg_scores(all_user_tests)

    draw_histogram(avg_scores)


def get_avg_scores(all_user_tests):
    if type(all_user_tests) != list:
        raise TypeError('get avg scores - all_user_tests type get', type(all_user_tests))

    avg_scores = {'en_google': 0, 'en_ljspeech': 0, 'en_milabs': 0, 'ch_google': 0, 'ch_mandarin': 0}

    for user_test in all_user_tests:
        avg_scores['en_google'] += user_test.en_google
        avg_scores['en_ljspeech'] += user_test.en_ljspeech
        avg_scores['en_milabs'] += user_test.en_milabs
        avg_scores['ch_google'] += user_test.ch_google
        avg_scores['ch_mandarin'] += user_test.ch_mandarin

    for key, value in avg_scores.items():
        avg_scores[key] = value / len(all_user_tests)

    return avg_scores


def draw_histogram(scores):
    if type(scores) != dict:
        raise TypeError('draw histogram - scores type get', type(scores))

    plt.bar(scores.keys(), scores.values())
    plt.title('TTS Scores')
    plt.xlabel('TTS')
    plt.ylabel('Score')
    plt.savefig('{0}/tts_score.png'.format(PATH['static']))
