from flask import jsonify


'''
response status:
200: OK
204: not login
400: request data format error
401: request data content error
500: undefined error
'''

response = {
    200: (jsonify({'status': True, 'message': 'success'}), 200),
    204: (jsonify({'status': False, 'message': 'not login'}), 204),
    400: (jsonify({'status': False, 'message': 'request data format error'}), 400),
    401: (jsonify({'status': False, 'message': 'request data content error'}), 401),
    500: (jsonify({'status': False, 'message': 'undefined error'}), 500)
}


def server_response(status_code, message=None):
    if status_code == 401 and message:
        change_response_message(401, message)

    return response[status_code]


def change_response_message(status_code, message):
    global response
    response[status_code] = (jsonify({'status': False, 'message': message}), status_code)

