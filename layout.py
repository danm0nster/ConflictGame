from nodebox.graphics import *
import math


class LayoutHelper:
    def __init__(self):
        # right margin for timer, expected payout and text, this makes "the main window" smaller by same amount
        # might need to be a calculated thing, but 200px for now
        self.right_margin = 200.0
        # margin from edges in px
        self.edge_margin = 50.0
        self.counter = 0

    def calculate_radius(self, padding):
        """ Calculates largest possible circle radius

        Calculates largest possible circle radius and subtract the padding value.
        Padding needs to be at least half the drawn objects size or it will be drawn outside of the screen
        values less than zero will be treated as zero

        Args:
           padding (int): Padding from edge in pixels, must be 0 or above
        Returns:
            float: radius of the circle
        """

        if padding < 0:
            padding = 0
        if canvas.height > (canvas.width-self.right_margin):
            # making sure there is room for the right margin
            radius = (canvas.width-self.right_margin)/2.0 - padding
        else:
            radius = canvas.height/2.0 - padding
        if radius < 0.0:
            return 0.0
        else:
            return radius

    def set_player_position(self, player_list):
        """ Set players position in a circle

        Spaces players out evenly in the largest circle given the layout constraints

        Args:
            player_list (list): list of the current players
        """
        # angle for the next draw, starts at 90 to get first draw to directly north
        angle = 90.0
        radius = self.calculate_radius(self.edge_margin)
        for player in player_list:
            angle_radians = math.radians(angle)
            origin_x = (canvas.width-self.right_margin)/2.0 - 25
            origin_y = canvas.height/2.0 - 25
            # x = originX + radius * cos(a)
            # TODO the 25 is half the drawing size of rect, needs changing
            x = origin_x + radius * math.cos(angle_radians) - self.edge_margin
            # y = originY + radius * sin(a)
            # TODO the 25 is half the drawing size of rect, needs changing
            y = origin_y + radius * math.sin(angle_radians) - self.edge_margin
            player.img.x = x
            player.img.y = y
            player.position = (x, y)
            angle += 360.0 / len(player_list)

    # TODO test for invalid input
    def draw_timer(self, elapsed_time, max_time, padding=10):
        """ Draws timer on the bottom right

        Args:
            elapsed_time(int): time elapsed since last reset in ms
            max_time(int): max time before reset in ms
        """
        length = self.right_margin - 2 * padding
        elapsed_length = (float(elapsed_time)/float(max_time)) * length

        # drawing the borders
        push()
        # TODO make it more clear
        translate(canvas.width - self.right_margin + padding, self.edge_margin)
        stroke(0, 1)
        nofill()
        strokewidth(2)
        # TODO insert height instead of 10
        rect(0, 0, length, 10)
        pop()

        # drawing elapsed bar
        push()
        # TODO insert height
        img = Image('pictures/red.png', x=canvas.width - self.right_margin + padding+1, y=self.edge_margin+1,
                    width=elapsed_length-1, height=8, data=None)
        image(img)
        pop()

    def draw_arrow(self, x0, y0, x1, y1):
        push()
        line(x0, y0, x1, y1)
        pop()
