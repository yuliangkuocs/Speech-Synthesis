# coding=UTF-8
from flask import Flask, render_template, url_for, session, redirect, request
from response import StatusCode, response
from generate_key import *
from voice import *
from user import *
from tts import tts

app = Flask(__name__)
app.secret_key = '7433a508b0a1ade2faea975e'

status_code = StatusCode()


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('text_to_speech'))
    return render_template('home.html')


@app.route('/about-us/')
def about_us():
    return render_template('about-us.html')


@app.route('/text-to-speech/')
def text_to_speech():
    if 'user_id' in session:
        return render_template('text-to-speech.html')
    else:
        return render_template('not-login.html')


@app.route('/private-policy/')
def private_policy():
    return render_template('private-policy.html')


@app.route('/login/')
def login():
    if 'user_id' in session:
        print('already login')
        return render_template('already-login.html')
    else:
        print('not login')
        return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/steven/')
def steven():
    return render_template('steven.html')


# API
# AUTH
@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    request_data = request.get_json()
    response_data = {}

    try:
        if 'id' not in request_data or 'password' not in request_data:
            return response(status_code.DATA_FORMAT_ERROR)

        user = select_user_by_id(request_data['id'])

        if not user:
            return response(status_code.DATA_CONTENT_ERROR, message='user not exists')

        if user.password != request_data['password']:
            return response(status_code.DATA_CONTENT_ERROR, message='wrong password')

        else:
            session['user_id'] = request_data['id']
            response_data['guid'] = user.guid
            return response(status_code.OK, response_data=response_data)

    except Exception as err:
        print('[ERROR - API] Login fail', err)
        return response(status_code.UNDEFINED)


@app.route('/api/auth/logout', methods=['GET'])
def api_auth_logout():
    request_data = request.get_json()

    try:
        if request_data:
            return response(status_code.DATA_FORMAT_ERROR)

        if 'user_id' not in session:
            return response(status_code.NOT_LOGIN)

        session.pop('user_id', None)
        return response(status_code.OK)

    except Exception as err:
        print('[ERROR - api/auth/logout]', err)
        return response(status_code.UNDEFINED)


@app.route('/api/auth/register', methods=['POST'])
def api_auth_register():
    request_data = request.get_json()

    try:
        if 'id' not in request_data or 'password' not in request_data:
            return response(status_code.DATA_FORMAT_ERROR)

        user = select_user_by_id(request_data['id'])

        if user:
            return response(status_code.DATA_CONTENT_ERROR, message='user already exists')

        else:
            guid = generate_guid()
            is_insert = insert_user(User(guid, request_data['id'], request_data['password']))

            if not is_insert:
                raise ValueError('[ERROR - api/auth/register] insert user fail')

            return response(status_code.OK)

    except Exception as err:
        print('[ERROR - api/auth/register]', err)
        return response(status_code.UNDEFINED)


# Voice
@app.route('/api/voice/tts', methods=['POST'])
def api_tts_mandarin():
    request_data = request.get_json()
    response_data = {}

    try:
        if 'guid' not in request_data or 'text' not in request_data or 'wav_name' not in request_data or 'tts_type' not in request_data:
            return response(status_code.DATA_FORMAT_ERROR)

        text = request_data['text']
        guid = request_data['guid']
        tts_type = request_data['tts_type']
        wav_name = request_data['wav_name']

        if not check_user(guid):
            return response(status_code.DATA_CONTENT_ERROR, message='user not exists')

        if not check_voice_name(guid, wav_name):
            return response(status_code.DATA_CONTENT_ERROR, message='wav name already exists')

        file_name = generate_voice_name(guid)

        tts(guid, text, file_name, TTS_TYPE[tts_type])

        voice = Voice(guid, file_name, wav_name, tts_type)

        is_insert = insert_voice(voice)

        if not is_insert:
            raise ValueError('insert voice fail')

        response_data['wav'] = get_voice_url(voice)

        return response(status_code.SUCCESS, response_data=response_data)

    except Exception as err:
        print('[ERROR - api/voice/tts]', err)
        return response(status_code.UNDEFINED)


@app.route('/api/voice/getAllWav', methods=['POST'])
def api_voice_getAllWav():
    request_data = request.get_json()
    response_data = {'wavs': {}}

    try:
        if 'guid' not in request_data:
            return response(status_code.DATA_FORMAT_ERROR)

        guid = request_data['guid']

        if not check_user(guid):
            return response(status_code.DATA_CONTENT_ERROR, message='user not exists')

        voices = select_voices_by_guid(guid)

        if voices:
            for voice in voices:
                response_data['wavs'][voice.wav_name] = get_voice_url(voice)

        return response(status_code.SUCCESS, response_data=response_data)

    except Exception as err:
        print('[ERROR - api/voice/getAllWav]', err)
        return response(status_code.UNDEFINED)


@app.route('/api/voice/delete', methods=['POST'])
def api_voice_delete():
    request_data = request.get_json()

    try:
        if 'guid' not in request_data or 'wav_name' not in request_data:
            return response(status_code.DATA_FORMAT_ERROR)

        guid = request_data['guid']
        wav_name = request_data['wav_name']

        if not check_user(guid):
            return response(status_code.DATA_CONTENT_ERROR, message='user not exists')

        voice = select_voice_by_wavname_and_guid(wav_name, guid)

        if not delete_voice(voice):
            raise IndexError('delete voice fail')

        return response(status_code.SUCCESS)

    except Exception as err:
        print('[ERROR - api/voice/getAllWav]', err)
        return response(status_code.UNDEFINED)


if __name__ == '__main__':
    print('create tables')
    create_tables()
    app.run(host='0.0.0.0', port=8080)
