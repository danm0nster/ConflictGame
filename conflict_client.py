from nodebox.graphics import *
from layout import LayoutHelper
from player import Player
from client_service import ClientService
from NetworkingClient import NetworkingClient
from time import time, sleep


def draw(canvas):
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
            # TODO remove test prints
            for p in service.player_list:
                print p.name

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
    pass

if __name__ == "__main__":
    layout = LayoutHelper()
    service = ClientService()
    network = NetworkingClient(service.domain)
    con = network.connect()
    # TODO should inverse both con and auth so that the program stops if either is None
    if con is not None:
        # TODO logging
        auth = network.authenticate(username=service.username, domain=service.domain, secret=service.secret)
        if auth is not None:
            # TODO logging
            pass
    network.send_message(to=service.server_jid, sender=service.jid, message="", subject="register")

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
