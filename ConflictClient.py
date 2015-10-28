from nodebox.graphics import *
import layout
import player
import math

players = [player.Player('a'), player.Player('b'), player.Player('c'), player.Player('d')]
layout_helper = layout.LayoutHelper()

def draw(canvas):
    canvas.clear()
    layout_helper.set_player_position(players)
    for player in players:
        push()
        strokewidth(2)
        stroke(0, 1)
        fill(1, 1)
        translate(50, 50)
        player.draw_self()
        nofill()
        pop()
    push()
    line(canvas.width - 200, 0, canvas.width - 200, canvas.height)
    nostroke()
    layout_helper.draw_timer(0, 10)
    translate(75, 75)
    layout_helper.draw_arrow(players[0].position[0], players[0].position[1], players[1].position[0], players[1].position[1])
    layout_helper.draw_arrow(players[2].position[0], players[2].position[1], players[3].position[0], players[3].position[1])
    layout_helper.draw_arrow(players[1].position[0], players[1].position[1], players[2].position[0], players[2].position[1])
    layout_helper.draw_arrow(players[3].position[0], players[3].position[1], players[0].position[0], players[0].position[1])
    layout_helper.draw_arrow(players[0].position[0], players[0].position[1], players[1].position[0], players[1].position[1])
    layout_helper.draw_arrow(players[0].position[0], players[0].position[1], players[2].position[0], players[2].position[1])
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
