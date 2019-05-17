# coding=UTF-8
import uuid
from flask import Flask, render_template, url_for, session, redirect, request
from response import StatusCode, response
from database.database import *

app = Flask(__name__)
app.secret_key = '7433a508b0a1ade2faea975e'

status_code = StatusCode()


# API
def generate_guid():
    '''
    generate guid for an user
    :return: str
    '''

    users = select_users()

    tell = True

    while True:
        guid = uuid.uuid4()

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
            is_insert = insert_user(User(guid, request_data['id'], request_data['password']))

            if not is_insert:
                raise ValueError('[ERROR - api/auth/register] insert user fail')

            return response(status_code.OK)

    except Exception as err:
        print('[ERROR - api/auth/register]', err)
        return response(status_code.UNDEFINED)


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=8080)
