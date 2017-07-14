import json
import threading

from Eden.Packet.Packet import Packet
from Eden.Controller.LoginController import LoginController


class Client(threading.Thread):
    connection = None
    address = None
    slot = None
    server = None
    character = None
    running = True

    def __init__(self, connection, address, slot, server):
        self.connection = connection
        self.address = address
        self.slot = slot
        self.server = server
        print("Connection accepted from " + self.address[0])
        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            try:
                data = self.connection.recv(1024)
                if not len(data) > 0:
                    continue
                new_data = data.decode("UTF-8").strip()
                packet = Packet.create_from_data(new_data)
                if packet.id == Packet.PACKET_ID_LOGIN:
                    controller = LoginController(self, packet)
                    controller.handle()
            except UnicodeDecodeError:
                print("Malformed packet")
                self.shutdown()
                break
            except json.decoder.JSONDecodeError:
                print("Malformed packet")
                self.shutdown()
                break

    def shutdown(self):
        self.running = False

    def is_logged_in(self):
        if not self.character is None:
            return True
        return False
