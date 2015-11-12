from player import Player
from client_service import ClientService
from time import time


class ServerService(ClientService):
    def __init__(self):
        super(ServerService, self).__init__()
        self.username = "server"
        self.__attack_dict = {}

    def add_attack(self, player0, player1):
        # Only add the attack if that player doesn't have a registered attack yet
        if player0 not in self.__attack_dict:
            self.__attack_dict[player0] = player1

    def flush_attacks(self):
        # TODO add data saving, temporarely will just clean that dict
        self.__attack_dict = {}

    def player_name_list(self):
        name_list = []
        for player in self.player_list:
            name_list.append(player.name)
        return name_list

    def generate_attack_string(self):
        msg = ''
        for key in self.__attack_dict:
            msg = msg + '::' + key.name
            msg = msg + '::' + self.__attack_dict[key].name
        return msg

    def elapsed_time(self):
        # Start the timer
        if not self.started:
            self.latest_time_tick = None
            return 0
        # sets the first timer
        if self.latest_time_tick is None:
            self.latest_time_tick = time()
            return 0
        # if there is a previous timer check elapsed time
        else:
            elapsed_time = time() - self.latest_time_tick
            # if elapsed_time is larger than the maximum time, reset timer
            if elapsed_time >= self.max_time:
                self.latest_time_tick = time()
            return elapsed_time
