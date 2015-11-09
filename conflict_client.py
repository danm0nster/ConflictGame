from nodebox.graphics import *
from layout import LayoutHelper
from player import Player
from client_service import ClientService
from NetworkingClient import NetworkingClient


def draw(canvas):
    if network.check_for_messages():
        message_handler()
    canvas.clear()
    push()
    strokewidth(1)
    stroke(0, 1)
    nofill()
    layout.set_player_position(service.player_list)
    for player in service.player_list:
        player.draw_self()
    layout.draw_right_margin()
    nostroke()
    if service.started:
        current_timer = service.elapsed_time()
        layout.draw_timer(current_timer, service.max_time)
        # if turn over reset clicked player
        if current_timer >= service.max_time:
            service.clicked_player = None
    #layout_helper.draw_arrow(players[0], players[1])
    #layout_helper.draw_arrow(players[3], players[0])
    #layout_helper.draw_arrow(players[3], players[1])
    #layout_helper.draw_arrow(players[2], players[3])
    #layout_helper.draw_arrow(players[1], players[2])
    #layout_helper.draw_arrow(players[1], players[3])
    #layout_helper.draw_arrow(players[0], players[2])
    #layout_helper.draw_arrow(players[2], players[0])
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

        # go to next message
        msg = network.pop_message()


def on_mouse_press(canvas, mouse):
    for player in service.player_list:
        if player.position[0] <= mouse.x <= (player.position[0] + player.img.width):
            if player.position[1] <= mouse.y <= (player.position[1] + player.img.height):
                service.clicked_player = player
                # TODO remove test print
                print 'clicked on player: ' + player.name
                if service.clicked_player is not None:
                    print service.clicked_player.name
                else:
                    print service.clicked_player


def on_key_press(canvas, keyboard):
    print "pressed a key"

if __name__ == "__main__":
    layout = LayoutHelper()
    service = ClientService()
    network = NetworkingClient(service.domain)
    con = network.connect()
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
    canvas.run(draw)
