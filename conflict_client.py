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
    #layout_helper.draw_timer(0, 10)
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

        msg = network.pop_message()


def on_mouse_press(canvas, mouse):
    print "mouse was clicked"
    print "x: ", mouse.x
    print "y: ", mouse.y


def on_key_press(canvas, keyboard):
    print "pressed a key"

if __name__ == "__main__":
    layout = LayoutHelper()
    service = ClientService()
    network = NetworkingClient(service.domain)
    print "username: " + service.username
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
