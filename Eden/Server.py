import socket
import sys
import threading
import time

from Eden.Client import Client


class Server(threading.Thread):
    game = None
    socket = None
    state = None
    slots = {}

    def __init__(self, game):
        self.game = game
        self.state = self.game.STATE_STARTING
        print("Starting server")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind(("localhost", 50705))
        except OSError:
            print("Something is already listen on the server port")
            sys.exit(1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setup_slots()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if self.game.state == self.game.STATE_RUNNING:
                break
            time.sleep(0.1)

        self.state = self.game.STATE_RUNNING
        print("Waiting for connections...")
        self.socket.listen(5)

        while self.state == self.game.STATE_RUNNING:
            try:
                (connection, address) = self.socket.accept()
                slot = self.find_next_slot()
                self.slots[slot] = Client(connection, address, slot, self)
                self.slots[slot].start()
            except socket.timeout:
                continue

        print("Server stopped")
        self.state = self.game.STATE_STOPPED

    def shutdown(self):
        print("Stopping server")
        self.state = self.game.STATE_STOPPING
        for i in range(0, 255):
            if self.slots[i] is None:
                continue
            self.slots[i].shutdown()

    def find_next_slot(self):
        for i in range(0, 255):
            if self.slots[i] is None:
                return i
        print("No more slots!")
        sys.exit(1)

    def setup_slots(self):
        for i in range(0, 255):
            self.slots[i] = None
