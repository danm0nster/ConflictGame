from nodebox.graphics import *
from nodebox.gui import *
import math


class LayoutHelper:
    def __init__(self, edge_margin=50.0, right_margin=200.0):
        # right margin for timer, expected payout and text, this makes "the main window" smaller by same amount
        # might need to be a calculated thing, but 200px for now
        self.right_margin = right_margin
        # margin from edges in px
        self.edge_margin = edge_margin
        self.counter = 0

    def draw_right_margin(self):
        self.right_margin
        line(canvas.width - self.right_margin, 0, canvas.width - self.right_margin, canvas.height)

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
            origin_x = (canvas.width-self.right_margin)/2.0 - player.img.width / 2.0
            origin_y = canvas.height/2.0 - player.img.height / 2.0
            # x = originX + radius * cos(a)
            x = origin_x + radius * math.cos(angle_radians)
            # y = originY + radius * sin(a)
            y = origin_y + radius * math.sin(angle_radians)
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
        if elapsed_length > length:
            elapsed_length = length

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

    def draw_arrow(self, player0, player1):
        """ Draws an arrow from a player to another player

        Args:
            player0 (Player): The player the arrow originates from
            player1 (Player): The player the arrow will go to
        """
        push()
        strokewidth(2)
        x0 = round(player0.position[0])
        y0 = round(player0.position[1])
        x1 = round(player1.position[0])
        y1 = round(player1.position[1])

        player0_anchor = []
        player1_anchor = []
        # find anchor points
        # goes from player0's corner to a mid point on player1
        if x0 > x1:
            # arrow going from east to west
            if y0 > y1:
                # arrow going SW
                player0_anchor.append(x0)
                player0_anchor.append(y0)
                player1_anchor.append(x1 + player1.img.width)
                player1_anchor.append(y1 + player1.img.height * 0.5)

            elif y1 > y0:
                # arrow going NW
                player0_anchor.append(x0)
                player0_anchor.append(y0 + player0.img.height)
                player1_anchor.append(x1 + player1.img.width * 0.5)
                player1_anchor.append(y1)
            elif y0 == y1:
                # W
                player0_anchor.append(x0)
                player0_anchor.append(y0)
                player1_anchor.append(x1 + player1.img.width)
                player1_anchor.append(y1 + player1.img.height * 0.5)

        elif x0 < x1:
            # arrow going from west to East
            if y0 > y1:
                # SE
                player0_anchor.append(x0 + player0.img.width)
                player0_anchor.append(y0)
                player1_anchor.append(x1 + player1.img.width * 0.5)
                player1_anchor.append(y1 + player1.img.height)
            elif y1 > y0:
                # NE
                player0_anchor.append(x0 + player0.img.width)
                player0_anchor.append(y0 + player0.img.height)
                player1_anchor.append(x1)
                player1_anchor.append(y1 + player1.img.height * 0.5)

            elif y0 == y1:
                # E
                player0_anchor.append(x0 + player0.img.width)
                player0_anchor.append(y0)
                player1_anchor.append(x1)
                player1_anchor.append(y1 + player1.img.height * 0.5)
        else:
            # going strictly north or south
            if y0 > y1:
                # South
                player0_anchor.append(x0)
                player0_anchor.append(y0)
                player1_anchor.append(x1 + player1.img.width * 0.5)
                player1_anchor.append(y1 + player1.img.height)
            else:
                # North
                player0_anchor.append(x0 + player0.img.width)
                player0_anchor.append(y0 + player0.img.height)
                player1_anchor.append(x1 + player1.img.width * 0.5)
                player1_anchor.append(y1)
        
        line(player0_anchor[0], player0_anchor[1], player1_anchor[0], player1_anchor[1])

        # making arrow heads
        dx = player1_anchor[0] - player0_anchor[0]
        dy = player1_anchor[1] - player0_anchor[1]
        angle_radians = math.atan2(dy, dx)
        degrees = math.degrees(angle_radians)
        fill(0, 1)
        # x = startX + length * cos(angle)
        # y = startY + length * sin(angle)
        # -180 degrees is from atan
        triangle1_x = player1_anchor[0] + 10 * math.cos(math.radians(-180 + degrees + 20))
        triangle1_y = player1_anchor[1] + 10 * math.sin(math.radians(-180 + degrees + 20))
        triangle2_x = player1_anchor[0] + 10 * math.cos(math.radians(-180 + degrees - 20))
        triangle2_y = player1_anchor[1] + 10 * math.sin(math.radians(-180 + degrees - 20))
        triangle(player1_anchor[0], player1_anchor[1], triangle1_x, triangle1_y, triangle2_x, triangle2_y)
        pop()

    def draw_expected_payout(self, expected_pay, padding=10):
        padding = padding
        push()
        txt = Text("Expected payout: " + str(expected_pay) + "kr.",
                   x=canvas.width - self.right_margin + padding,
                   y=canvas.height-self.edge_margin,
                   width=self.right_margin - 2*padding,
                   height=10)
        txt.style(0, len(txt.text), fill=Color(0, 0, 0), align=RIGHT)
        txt.fontname = "Droid Sans"
        txt.fontsize = 11
        text(txt)
        pop()

    def draw_start_stop_button(self, caption, action=None, padding=10):
        # TODO on y, the 10 is from the timer, should not be static
        button = Button(caption=caption,
                        action=action,
                        x=canvas.width - self.right_margin + padding,
                        y=self.edge_margin + 10 + padding,
                        width=self.right_margin - 2 * padding,
                        id='start_stop_button')
        canvas.append(button)

    def change_start_stop_text(self, value):
        for item in canvas:
            if item.id == 'start_stop_button':
                item.caption = value
