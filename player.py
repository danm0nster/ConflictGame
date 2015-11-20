from nodebox.graphics import *


class Player:
    def __init__(self, name):
        self.name = name
        # TODO make position a property that updates image position
        self.position = None
        self.img = Image('pictures/squirrel.png', x=0, y=0,
                    width=50, height=50, data=None)

    def draw_self(self, highlight=False):
        push()
        if highlight:
            # the +1's are due to the increased strokewidth
            rect(self.img.x-1,
                 self.img.y-1,
                 self.img.width + 2,
                 self.img.height + 2,
                 stroke=Color(0, 0, 0, 1),
                 strokewidth=2)
        image(self.img)
        pop()
