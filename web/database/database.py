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
            FILE_NAME   TEXT                    NOT NULL,
            WAV_NAME    TEXT                    NOT NULL,
            TTS_TYPE    INT                     NOT NULL);
        '''
    )

    db_connect.commit()
    db_connect.close()


def sql_to_data(db_users=None, db_voices=None, db_user=None, db_voice=None):
    if db_users:
        users = [User(db_user[0], db_user[1], db_user[2]) for db_user in db_users]

        return users

    elif db_voices:
        voices = [Voice(db_voice[0], db_voice[1], db_voice[2], db_voice[3]) for db_voice in db_voices]

        return voices

    elif db_user:
        user = User(db_user[0], db_user[1], db_user[2])

        return user

    elif db_voice:
        voice = Voice(db_voice[0], db_voice[1], db_voice[2], db_voice[3])

        return voice

    return None


# User
def select_users():
    """
    select all users
    :return: [User]
    """

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM User')

    users = sql_to_data(db_users=db_cursor.fetchall())

    db_connect.close()

    return users


def select_user_by_id(id):
    """
    select an user by id
    :param id: user id
    :return: User
    """

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM User WHERE ID = \'%s\'' % id)
    user = sql_to_data(db_user=db_cursor.fetchone())

    db_connect.close()

    return user


def select_user_by_guid(guid):
    """
    select an user by guid
    :param guid: user guid
    :return: User
    """

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM User WHERE GUID = \'%s\'' % guid)
    user = sql_to_data(db_user=db_cursor.fetchone())

    db_connect.close()

    return user


def insert_user(user):
    """
    insert an user into table User
    :param user: User
    :return: Bool
    """

    is_insert = True

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    try:
        db_cursor.execute('INSERT INTO User (GUID, ID, PASSWORD) VALUES (\'%s\', \'%s\', \'%s\');' % (
            user.guid, user.id, user.password))

    except sqlite3.Error as err:
        print('[ERROR - DB] Insert an user fail:', err)
        is_insert = False

    db_connect.commit()
    db_connect.close()

    return is_insert


# Voice
def select_voices():
    """
    select all voices
    :return: [Voice]
    """

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM Voice')

    voices = sql_to_data(db_voices=db_cursor.fetchall())

    db_connect.close()

    return voices


def select_voices_by_guid(guid):
    """
    select all voices owned by the user with guid
    :param guid: user guid
    :return: [Voice]
    """

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM Voice WHERE GUID = \'%s\'' % guid)

    voices = sql_to_data(db_voices=db_cursor.fetchall())

    db_connect.close()

    return voices


def select_voice_by_filename_and_guid(file_name, guid):
    """
    select a voice with the file_name owned by the user with guid
    :param file_name: voice file_name
    :param guid: user guid
    :return: Voice
    """

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    db_cursor.execute('SELECT * FROM Voice WHERE GUID = \'%s\' AND FILE_NAME =  \'%s\'' % (guid, file_name))
    voice = sql_to_data(db_voice=db_cursor.fetchone())

    db_connect.close()

    return voice


def insert_voice(voice):
    """
    insert an voice into table Voice
    :param voice: Voice
    :return: Bool
    """

    is_insert = True

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    try:
        db_cursor.execute('INSERT INTO Voice (GUID, FILE_NAME, WAV_NAME, TTS_TYPE) VALUES (\'%s\', \'%s\', \'%s\', %d);' % (
            voice.guid, voice.file_name, voice.wav_name, voice.tts_type))

    except sqlite3.Error as err:
        print('[ERROR - DB] Insert an voice fail:', err)
        is_insert = False

    db_connect.commit()
    db_connect.close()

    return is_insert


def delete_voice_by_filename_and_guid(file_name, guid):
    """
    delete a voice with the file_name owned by the user with guid
    :param file_name: voice file_name
    :param guid: user guid
    :return: Bool
    """

    is_delete = True

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    try:
        db_cursor.execute('DELETE FROM Voice WHERE GUID = \'%s\' AND FILE_NAME = \'%s\'' % (guid, file_name))

    except sqlite3.Error as err:
        print('[ERROR - DB] Delete an voice fail:', err)
        is_delete = False

    db_connect.commit()
    db_connect.close()

    return is_delete


def delete_voices_by_guid(guid):
    """
    delete a voice with the file_name owned by the user with guid
    :param guid: user guid
    :return: Bool
    """

    is_delete = True

    db_connect = sqlite3.connect(DATABASE)
    db_cursor = db_connect.cursor()

    try:
        db_cursor.execute('DELETE FROM Voice WHERE GUID = \'%s\'' % guid)

    except sqlite3.Error as err:
        print('[ERROR - DB] Delete voices fail:', err)
        is_delete = False

    db_connect.commit()
    db_connect.close()

    return is_delete
