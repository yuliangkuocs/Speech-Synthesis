# coding=UTF-8
import random
import string
from flask import request, session
from index import app
from response import StatusCode, response
from database.database import *

status_code = StatusCode()


def generate_guid():
    '''
    generate guid for an user with size 32
    :return: str
    '''

    chars = string.ascii_lowercase + string.digits

    users = select_users()

    tell = True

    while True:
        guid = ''.join(random.choices(chars, k=32))

        if users:
            for u in users:
                if guid == u.guid:
                    tell = False
                    break

            if not tell:
                tell = True
                continue

        break

    return guid


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
            insert_user(User(guid, request_data['id'], request_data['password']))

    except Exception as err:
        print('[ERROR - api/auth/logout]', err)
        return response(status_code.UNDEFINED)
