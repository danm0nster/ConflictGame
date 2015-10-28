from nodebox.graphics import *


class Player:
    def __init__(self, name):
        self.name = name
        # TODO make position a property that updates image position
        self.position = None
        self.img = Image('pictures/squirrel.png', x=0, y=0,
                    width=50, height=50, data=None)

    def draw_self(self):
        image(self.img)

    def get_height(self):
        return self.img.height
