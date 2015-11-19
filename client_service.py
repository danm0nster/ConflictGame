from player import Player
import time


class ClientService(object):
    def __init__(self):
        # TODO change player list to property?
        self.player_list = []
        # TODO cfg file import of username and other configs?
        # TODO split into common service? username + clicked_player + find_self
        # TODO maybe include previous round into the split, depending on server handling
        self._MAX_TIME = 6
        self._USERNAME = 'test2'
        self._DOMAIN = 'YLGW036484'
        self._SECRET = "1234"
        self._SERVER_NAME = "server"
        self.timestamp = None
        self._started = False
        self._clicked_player = None
        self.previous_round = None

    @property
    def max_time(self):
        return self._MAX_TIME

    @max_time.setter
    def max_time(self, max_time):
        self._MAX_TIME = max_time

    @property
    def username(self):
        return self._USERNAME

    @username.setter
    def username(self, username):
        self._USERNAME = username

    @property
    def domain(self):
        return self._DOMAIN

    @domain.setter
    def domain(self, domain):
        self._DOMAIN = domain

    @property
    def jid(self):
        return self.username + "@" + self.domain.lower()

    @property
    def server_jid(self):
        return self.server_name + "@" + self.domain

    @property
    def secret(self):
        return self._SECRET

    @secret.setter
    def secret(self, secret):
        self._SECRET = secret

    @property
    def server_name(self):
        return self._SERVER_NAME

    # TODO not sure servername should have a setter
    @server_name.setter
    def server_name(self, server_name):
        self._SERVER_NAME = server_name

    @property
    def started(self):
        return self._started

    @started.setter
    def started(self, value):
        if value is False or value is True:
            self._started = value

    def elapsed_time(self):
        """ Finds the delta in time since the last timestamp

        If the game is not started it resets timestamp to None and returns 0.
        If the game is started but the timestamp is None, make the first timestamp to the current time.
        Otherwise it will return the amount of time since the timestamp in seconds.

        Returns:
            int: if the game is not started it returns 0
            int: if the game is started but no timestamp exist, create one and return 0
            float: returns the time since the timestamp in seconds

        """
        # reset timer if game is not started
        if not self.started:
            self.timestamp = None
            return 0
        # sets the first timer
        if self.timestamp is None:
            self.timestamp = time.time()
            return 0
        # if there is a previous timer check elapsed time
        else:
            elapsed_time = time.time() - self.timestamp
            # if elapsed_time is larger than the maximum time, reset timer
            if elapsed_time >= self.max_time:
                self.timestamp = self.max_time
            return elapsed_time

    @property
    def clicked_player(self):
        return self._clicked_player

    @clicked_player.setter
    def clicked_player(self, player):
        if self._clicked_player is None:
            self._clicked_player = player
        if player is None and self._clicked_player is not None:
            self._clicked_player = player

    def find_player(self, name):
        """ Searches the list of players for a given name

        Returns the first instance where a player has the given name.

        Args:
            name (string): the name of the player you want to find

        Returns:
            Player: the Player object with the given name
        """
        for index in range(0, len(self.player_list)):
            if self.player_list[index].name == name:
                return self.player_list[index]

    def find_self(self):
        """ Find yourself from the player list

        Return:
            Player: the Player of yourself.
        """
        for index in range(0, len(self.player_list)):
            if self.player_list[index].name == self.jid:
                return self.player_list[index]
