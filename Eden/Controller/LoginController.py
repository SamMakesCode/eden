from Eden.Model.Character import Character
from Eden.Except.BadLogin import BadLogin


class LoginController:
    packet = None

    def __init__(self, client, packet):
        self.client = client
        self.packet = packet

    def handle(self):
        username = self.packet.data["username"]
        password = self.packet.data["password"]
        character = Character.read_using_username(username)
        if not character.password == password:
            raise BadLogin("Username/password combination is bad")
        self.client.character = character
