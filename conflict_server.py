# -*- coding: utf-8 -*-
from nodebox.graphics import *
from server_service import ServerService
from layout import LayoutHelper
from NetworkingClient import NetworkingClient
from time import sleep
from player import Player


def draw(canvas):
    """The method used by Nodebox to draw to the screen

    This method is called by canvas will be run a number of times pr second
    equal to the fps that has been set.
    If the computer is not powerful enough it will be runned as many times as possible
    each second.
    """
    # Checks for network messages and handles them
    if network.check_for_messages():
        message_handler()
    layout.set_player_position(service.player_list)
    push()
    strokewidth(1)
    stroke(0, 1)
    nofill()
    for player in service.player_list:
        player.draw_self()
    layout.draw_right_margin()
    # timer handling
    if service.started:
        current_timer = service.elapsed_time()
        layout.draw_timer(current_timer, service.max_time)
        # if turn over reset clicked player
        if current_timer >= service.max_time:
            canvas.clear()
            network.send_mass_messages(service.player_name_list(),
                                       service.server_jid,
                                       message=service.generate_attack_string(),
                                       subject='round_result')
            service.flush_attacks()
            network.send_mass_messages(service.player_name_list(),
                                       service.server_jid,
                                       message='',
                                       subject='new_round')
    pop()


def message_handler():
    """Handles network messages

    This method handles messages from the network layer and removes them
    after responding to them.
    """
    msg = network.pop_message()
    while msg is not None:
        # new player registers
        if msg.subject[:8] == 'register':
            # TODO service or network method to remove jid?
            if not service.started:
                player_name = msg.sender.getStripped()
                service.player_list.append(Player(name=str(player_name)))

        if msg.subject[:8] == 'attacked':
            players = msg.body.split('::')
            player0 = service.find_player(players[0])
            player1 = service.find_player(players[1])
            service.add_attack(player0, player1)
            layout.draw_arrow(player0, player1)
        # msg handling above here
        msg = network.pop_message()


def start_stop_button_action(button):
    """handles mouse presses on the start/stop button

    If the game is stopped it will start the game and change the label of the button
    If the game is started it will stop the current game and change the label of the button
    """
    # first it changes if it's started or not
    service.started = not service.started
    # Then takes appropriate actions
    if service.started:
        layout.change_start_stop_text('Stop')
        # resets aggression matrix when starting
        service.aggression_matrix = None
    else:
        layout.change_start_stop_text('Start')

    if service.started:
        player_names = ''
        for player in service.player_list:
            # TODO inserting :: as a message delimiter
            player_names = player_names + '::' + player.name
        # sends list of all players to all participants
        network.send_mass_messages(service.player_name_list(),
                                   service.server_jid,
                                   message=player_names,
                                   subject="start")
        service.generate_aggression_matrix()
        service.database.start_experimental_session("x", "x", "Dan Mønster", service.server_version)
        service.insert_session(service.experimental_round, game_phase=True)
        service.start_game_phase()
        service.register_jids()
    else:
        service.end_game_phase()


if __name__ == "__main__":
    service = ServerService()
    layout = LayoutHelper()
    network = NetworkingClient(service.domain)
    con = network.connect()
    if con is None:
        raise RuntimeError('Can\'t connect to the network')
    auth = network.authenticate(username=service.username, domain=service.domain, secret=service.secret)
    if auth is None:
        raise RuntimeError('Can\'t authenticate with given username and password')
    canvas.fps = 30
    canvas.fullscreen = False
    if service.started:
        layout.draw_start_stop_button('Stop', action=start_stop_button_action)
    else:
        layout.draw_start_stop_button('Start', action=start_stop_button_action)
    # deleting offline messages
    # need to have a small delay so that it will receive them before it start drawing
    sleep(0.2)
    while network.check_for_messages():
        network.pop_message()
    canvas.run(draw)
