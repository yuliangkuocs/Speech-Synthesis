import os
from database.database import *
from database.model import User
from path import PATH


def check_user(guid):
    user = select_user_by_guid(guid)

    if not user:
        return False

    return True


def delete_user(user):
    try:
        check_user_type(user)

        if not check_user(user.guid):
            raise ValueError('user not exists')

        delete_user_by_guid(user.guid)

        user_path = os.path.join(PATH['web_static'], user.guid)

        os.system('rm -rf %s' % user_path)

    except Exception as err:
        print('[ERROR - user] delete user fail:', err)
        return False

    return True


def check_user_type(user):
    if type(user) != User:
        raise TypeError('type must be \'User\', but get \'{0}\''.format(type(user)))
