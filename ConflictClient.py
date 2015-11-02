from nodebox.graphics import *
import layout
import player
import math

players = [player.Player('a'), player.Player('b'), player.Player('c'), player.Player('d'), player.Player('a'), player.Player('b'), player.Player('c'), player.Player('d'), player.Player('a'), player.Player('b'), player.Player('c'), player.Player('d')]
layout_helper = layout.LayoutHelper()


def draw(canvas):
    canvas.clear()
    layout_helper.set_player_position(players)
    for player in players:
        push()
        strokewidth(1)
        stroke(0, 1)
        fill(1, 1)
        player.draw_self()
        nofill()
        pop()
    push()
    layout_helper.draw_right_margin(right_margin=200.0)
    nostroke()
    layout_helper.draw_timer(0, 10)
    #layout_helper.draw_arrow(players[0], players[1])
    #layout_helper.draw_arrow(players[3], players[0])
    #layout_helper.draw_arrow(players[3], players[1])
    layout_helper.draw_arrow(players[2], players[3])
    #layout_helper.draw_arrow(players[1], players[2])
    #layout_helper.draw_arrow(players[1], players[3])
    #layout_helper.draw_arrow(players[0], players[2])
    #layout_helper.draw_arrow(players[2], players[0])
    layout_helper.draw_expected_payout(130)
    pop()


def on_mouse_press(canvas, mouse):
    print "mouse was clicked"
    print "x: ", mouse.x
    print "y: ", mouse.y


def on_key_release(canvas, keyboard):
    print "released a key"


def on_key_press(canvas, keyboard):
    print "pressed a key"


canvas.on_key_press = on_key_press
canvas.on_key_release = on_key_release
canvas.on_mouse_press = on_mouse_press
canvas.fps = 30
canvas.fullscreen = False
canvas.run(draw)
