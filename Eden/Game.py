import time

from Eden.Server import Server
from Eden.Handler.NPCHandler import NPCHandler


class Game:
    STATE_STOPPED = 1
    STATE_STARTING = 2
    STATE_RUNNING = 3
    STATE_STOPPING = 4

    npc_handler = None
    server = None
    state = STATE_STOPPED

    def __init__(self):
        print("Starting game...")
        self.state = self.STATE_STARTING
        self.npc_handler = NPCHandler()
        self.server = Server(self)
        self.server.start()

    def run(self):
        print("Playing game...")
        self.state = self.STATE_RUNNING
        while self.state == self.STATE_RUNNING:
            self.npc_handler.process()
            time.sleep(1)

    def shutdown(self):
        self.state = self.STATE_STOPPING
        self.server.shutdown()
        while True:
            if self.server.state == self.STATE_STOPPED:
                break
            time.sleep(0.1)
        print("Stopping game...")
        self.npc_handler.shutdown()
        print("Game stopped")
