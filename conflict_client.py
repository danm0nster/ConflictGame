# -*- coding: utf-8 -*-
from nodebox.graphics import *
from layout import LayoutHelper
from player import Player
from client_service import ClientService
from NetworkingClient import NetworkingClient
from time import time, sleep


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
    canvas.clear()
    push()
    strokewidth(1)
    stroke(0, 1)
    nofill()
    layout.set_player_position(service.player_list)
    for player in service.player_list:
        if player.name == service.find_self().name:
            player.draw_self(highlight=True)
        else:
            player.draw_self()
    layout.draw_right_margin()
    if service.previous_round is not None:
        # iterating through previous attacks
        for key in service.previous_round:
            push()
            strokewidth(0.5)
            stroke(0.5, 0.5, 0.5, 0.5)
            # checks if the iteration is at your attack
            if key != service.find_self().name:
                # if you haven't chosen a target to attack yet, draw your the previous attack
                if service.clicked_player is None:
                    layout.draw_arrow(service.find_player(key), service.find_player(service.previous_round[key]))
                else:
                    # if you attack a different target than in the previous round, draw your previous attack
                    if service.find_player(service.previous_round[key]).name != service.clicked_player.name:
                        layout.draw_arrow(service.find_player(key), service.find_player(service.previous_round[key]))
            else:
                # draw a users previous attack
                layout.draw_arrow(service.find_player(key), service.find_player(service.previous_round[key]))
            pop()
    if service.clicked_player is not None:
        push()
        strokewidth(1)
        stroke(0, 1)
        layout.draw_arrow(service.find_self(), service.clicked_player)
        pop()
    # timer
    if service.started:
        current_timer = service.elapsed_time()
        layout.draw_timer(current_timer, service.max_time)
    layout.draw_expected_payout(130)
    pop()


def message_handler():
    """Handles network messages

    This method handles messages from the network layer and removes them
    after responding to them.
    """
    msg = network.pop_message()
    while msg is not None:
        if msg.subject[:5] == 'start':
            # split the message into list of JID's
            players = msg.body.split('::')
            for player in players:
                if player != '':
                    # removing resource part of the jid for clean names without resource identifier
                    name = player.split('/')[0]
                    new_player = Player(name=name)
                    service.player_list.append(new_player)
            service.started = True

        if msg.subject[:12] == 'round_result':
            # split the message into a dict of attacks
            attacks = msg.body.split('::')
            attack_dict = {}
            # TODO counter starts at one since first entry will be empty
            counter = 1
            # recreate the attack dictionary from the server
            while counter < len(attacks) - 1:
                attack_dict[attacks[counter]] = attacks[counter+1]
                counter = counter + 1
            service.previous_round = attack_dict

        if msg.subject[:9] == 'new_round':
            service.clicked_player = None
            service.timestamp = time()

        # go to next message
        msg = network.pop_message()


def on_mouse_press(canvas, mouse):
    """ Handles mouse press

    This method handles mouse presses during run time
    If a legal player is clicked it will set the users attack to that player
    otherwise it does nothing

    Args:
        canvas(canvas): global canvas variable provided by nodebox library
        mouse(mouse): mouse variable provided by nodebox library
    """
    # finds what player was clicked
    for player in service.player_list:
        if player.position[0] <= mouse.x <= (player.position[0] + player.img.width):
            if player.position[1] <= mouse.y <= (player.position[1] + player.img.height):
                myself = service.find_self()
                if player.name != myself.name:
                    service.clicked_player = player
                    layout.draw_arrow(myself, player)
                    msg = myself.name + "::" + player.name
                    # informs the server of the attack
                    network.send_message(to=service.server_jid, sender=service.jid, message=msg, subject="attacked")
                # TODO remove test print
                print 'clicked on player: ' + player.name
                if service.clicked_player is not None:
                    print service.clicked_player.name
                else:
                    print service.clicked_player


def on_key_press(canvas, keyboard):
    """Method to handle keyboard presses during run time

    Currently does nothing on keypress
    """
    pass

if __name__ == '__main__':
    layout = LayoutHelper()
    service = ClientService()
    network = NetworkingClient(service.domain)
    con = network.connect()
    if con is None:
        raise RuntimeError('Can\'t connect to the network')
    auth = network.authenticate(username=service.username, domain=service.domain, secret=service.secret)
    if auth is None:
        raise RuntimeError('Can\'t authenticate with given username and password')
    network.send_message(to=service.server_jid, sender=service.jid, message=str(service.version), subject="register")

    canvas.on_key_press = on_key_press
    canvas.on_mouse_press = on_mouse_press
    canvas.fps = 30
    canvas.fullscreen = False
    # deleting offline messages
    # need to have a very little delay so that it will receive them before it start drawing
    sleep(0.2)
    while network.check_for_messages():
        network.pop_message()
    canvas.run(draw)
