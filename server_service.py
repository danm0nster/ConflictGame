from player import Player
from client_service import ClientService


class ServerService(ClientService):
    def __init__(self):
        super(ServerService, self).__init__()
        self.username = "server"
