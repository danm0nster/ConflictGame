from player import Player
from client_service import ClientService
from time import time
import numpy


class ServerService(ClientService):
    def __init__(self):
        super(ServerService, self).__init__()
        self.database = self.DatabaseManager()
        self.username = "server"
        self._attack_dict = {}
        self.aggression_matrix = None
        self.cumulative_matrix = None

    def add_attack(self, player0, player1):
        # Only add the attack if that player doesn't have a registered attack yet
        if player0 not in self._attack_dict:
            self._attack_dict[player0] = player1

    def flush_attacks(self):
        self.aggression_matrix = self.generate_aggression_matrix()
        self.add_to_cumulative_matrix(self.aggression_matrix)
        # TODO remove test print
        print 'aggression matrix: ', self.aggression_matrix
        print 'cumulative atrix: ', self.cumulative_matrix
        # TODO add data saving, temporarely will just clean that dict
        self._attack_dict = {}

    def player_name_list(self):
        name_list = []
        for player in self.player_list:
            name_list.append(player.name)
        return name_list

    def generate_attack_string(self):
        msg = ''
        for key in self._attack_dict:
            msg = msg + '::' + key.name
            msg = msg + '::' + self._attack_dict[key].name
        return msg

    def elapsed_time(self):
        # Start the timer
        if not self.started:
            self.timestamp = None
            return 0
        # sets the first timer
        if self.timestamp is None:
            self.timestamp = time()
            return 0
        # if there is a previous timer check elapsed time
        else:
            elapsed_time = time() - self.timestamp
            # if elapsed_time is larger than the maximum time, reset timer
            if elapsed_time >= self.max_time:
                self.timestamp = time()
            return elapsed_time

    def generate_aggression_matrix(self):
        # TODO poor performance for now, look into this
        # O(n^3) ouch, you can do better than this, but make the rest work first
        # makes an array the size of self.player_list fills it with 0's
        temp_array = [0] * len(self.player_list)
        # then every entry in the array will be changed to a new array filled with zeroes
        # this array has the size of self.player_list, this makes a n x n array with n = len(self.player_list)
        for entry in range(0, len(temp_array)):
            temp_array[entry] = [0] * len(self.player_list)
        for attack in self._attack_dict:
            # start by finding the indexes of the players
            attacker = None
            defender = None
            found = False
            while not found:
                for index in range(0, len(self.player_list)):
                    if self.player_list[index].name == attack.name:
                        attacker = index
                    elif self.player_list[index].name == self._attack_dict[attack].name:
                        defender = index
                    if attacker is not None and defender is not None:
                        found = True
                # attacker goes to the x and defender to the y
                temp_array[attacker][defender] = 1
                # next 2 statements is not needed, but will show if there is an error
                attacker = None
                defender = None
        return temp_array

    def add_to_cumulative_matrix(self, aggression_matrix):
        if aggression_matrix is not None and self.cumulative_matrix is not None:
            self.cumulative_matrix = numpy.add(aggression_matrix, self.cumulative_matrix)
        else:
            self.cumulative_matrix = aggression_matrix

    class DatabaseManager(object):
        def __init__(self):
            try:
                file = open('db_settings.ini', 'r')
                lines = file.readlines()
                # for each relevant line, it checks it the formatting is appropiate
                # it does this by substringing the line and checking the value vs the expected value
                # if it's wrong it raises an exception saying that the db_settings file is malformed
                if lines[0][:5] != 'user=':
                    raise IOError('db_settings malformed')
                if lines[1][:9] != 'password=':
                    raise IOError('db_settings malformed')
                if lines[2][:3] != 'db=':
                    raise IOError('db_settings malformed')
                # initiates variables to the values in the settings file
                self.user = lines[0][5:]
                self.secret = lines[1][9:]
                self.db = lines[2][3:]
            except IOError:
                # TODO message informing user that it can't connect to the database
                pass

