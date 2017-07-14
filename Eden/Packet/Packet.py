import json


class Packet:
    PACKET_ID_LOGIN = 1

    id = None
    data = {}

    def set_id(self, id):
        self.id = id

    def push_data(self, key, value):
        self.data[key] = value

    def export(self):
        packet = json.dumps(
            {
                'id': self.id,
                'data': self.data,
            }
        )
        return packet

    @staticmethod
    def create_from_data(data):
        packet = json.loads(data)
        instance = Packet()
        print(packet)
        instance.id = packet["id"]
        instance.data = packet["data"]
        return instance
