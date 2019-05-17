# coding=UTF-8
import sqlite3
from database.model import *

DATABASE = 'database.db'


def create_tables():
    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS User (
            GUID        TEXT    PRIMARY KEY     NOT NULL,
            ID          TEXT    UNIQUE          NOT NULL,
            PASSWORD    TEXT                    NOT NULL);
        '''
    )

    db_cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Voice (
            GUID        TEXT                    NOT NULL,
            NAME        TEXT                    NOT NULL);
        '''
    )

    db_connect.commit()
    db_connect.close()


def sql_to_data(db_users=None, db_voices=None, db_user=None, db_voice=None):
    if db_users:
        users = [User(db_user[0], db_user[1], db_user[2]) for db_user in db_users]

        return users

    elif db_voices:
        voices = [Voice(db_voice[0], db_voice[1]) for db_voice in db_voices]

        return voices

    elif db_user:
        user = User(db_user[0], db_user[1], db_user[2])

        return user

    elif db_voice:
        voice = Voice(db_voice[0], db_voice[1])

        return voice

    return None


def select_users():
    '''
    select all users
    :return: [User]
    '''

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM User')

    users = sql_to_data(db_users=db_cursor.fetchall())

    db_connect.close()

    return users


def select_user_by_id(id):
    '''
    select an user by id
    :param id: user id
    :return: User
    '''

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM User WHERE ID = \'%s\'' % id)
    user = sql_to_data(db_user=db_cursor.fetchone())

    db_connect.close()

    return user


def insert_user(user):
    '''
    insert an user into table User
    :param user: User
    :return: Bool
    '''

    is_insert = True

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    try:
        db_cursor.execute('INSERT INTO User (GUID, ID, PASSWORD) VALUES (\'%s\', \'%s\', \'%s\');' % (user.guid, user.id, user.password))

    except sqlite3.Error as err:
        print('[ERROR - DB] Insert an user fail:', err)
        is_insert = False

    db_connect.commit()
    db_connect.close()

    return is_insert

