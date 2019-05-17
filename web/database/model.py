# coding=UTF-8
class User:
    def __init__(self, guid=None, id=None, password=None):
        self.guid = guid
        self.id = id
        self.password = password


class Voice:
    def __init__(self, guid=None, name=None):
        self.guid = guid
        self.name = name