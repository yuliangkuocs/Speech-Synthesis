import uuid
from database.database import *


def generate_guid():
    """
    generate a unique guid for an user
    :return: str
    """

    while True:
        guid = uuid.uuid4()

        if not select_user_by_guid(guid):
            return str(guid)


def generate_voice_name(guid):
    """
    generate a unique voice name for an user
    :param guid: user guid
    :return: voice name
    """

    while True:
        file_name = uuid.uuid4()

        if not select_voice_by_filename_and_guid(file_name, guid):
            return str(file_name)
