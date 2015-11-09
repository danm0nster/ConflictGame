from nodebox.graphics import *
from server_service import ServerService
from layout import LayoutHelper
from NetworkingClient import NetworkingClient
from NetworkingClient import Message
from player import Player


def draw(canvas):
    if network.check_for_messages():
        message_handler()
    canvas.clear()
    layout.set_player_position(service.player_list)
    push()
    strokewidth(1)
    stroke(0, 1)
    nofill()
    for player in service.player_list:
        player.draw_self()
    layout.draw_right_margin()
    layout.draw_timer(service.elapsed_time(), service.max_time)
    pop()
    # TODO draw timer


def message_handler():
    msg = network.pop_message()
    while msg is not None:
        # new player registers
        if msg.subject[:8] == 'register':
            service.player_list.append(Player(name=str(msg.sender)))

        # msg handling above here
        msg = network.pop_message()


def start_stop_button_action(button):
    service.started = not service.started
    if service.started:
        layout.change_start_stop_text('Stop')
    else:
        layout.change_start_stop_text('Start')

    if service.started:
        all_players = []
        player_names = ''
        for player in service.player_list:
            all_players.append(player.name)
            # inserting :: as a message delimiter
            player_names = player_names + '::' + player.name
        # sends list of all players to all participants
        network.send_mass_messages(all_players, service.server_jid, message=player_names, subject="start")


if __name__ == "__main__":
    service = ServerService()
    layout = LayoutHelper()
    network = NetworkingClient(service.domain)
    con = network.connect()
    if con is not None:
        # TODO logging
        auth = network.authenticate(username=service.username, domain=service.domain, secret=service.secret)
        if auth is not None:
            # TODO logging
            pass
    canvas.fps = 30
    canvas.fullscreen = False
    if service.started:
        layout.draw_start_stop_button('Stop', action=start_stop_button_action)
    else:
        layout.draw_start_stop_button('Start', action=start_stop_button_action)
    canvas.run(draw)


    # TODO delete scratchpad below
    #var1 = ClientService()
    #var2 = ServerService()

    #print var2.username
    #print "changing var 1"
    #var1.username = "kurt"
    #print "var 1 is: " + var1.username
    #print "var 2 is:" + var2.username
    #print "var 2 time: " + str(var2.max_time)
    #print "" + str(var2.player_list)