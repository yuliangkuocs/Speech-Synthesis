# coding=UTF-8
from flask import jsonify

response_message = {200: 'success',
                    204: 'not login',
                    400: 'data format error',
                    401: 'data content error',
                    500: 'undefined error'}


def response(status_code, message=None, response_data=None):
    if response_data and type(response_data) != dict:
        raise TypeError('response data must be dict')

    if status_code == StatusCode().DATA_CONTENT_ERROR and not message:
        raise ValueError('data content error must have message to tell which content is wrong')

    result = {'status': True if status_code == 200 else False,
              'message': response_message[status_code] if not message else message,
              'response': response_data if response_data else {}}

    return jsonify(result), status_code


class StatusCode:
    def __init__(self):
        self.OK = self.SUCCESS = 200
        self.NOT_LOGIN = 204
        self.DATA_FORMAT_ERROR = 400
        self.DATA_CONTENT_ERROR = 401
        self.UNDEFINED = 500
