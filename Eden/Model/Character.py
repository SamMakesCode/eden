import json


class Character:
    username = None
    password = None

    def __init__(self):
        ''' sad '''

    @staticmethod
    def read_using_username(username):
        instance = Character()
        file_content = open('./data/characters/' + username + '.json').read()
        unbusted = json.loads(file_content)
        instance.username = unbusted["username"]
        instance.password = unbusted["password"]
        return instance
