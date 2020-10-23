import random
import math
import time

from Sprites import *


class Displacement:
    def __init__(self):
        self.last_direction = None
        self.north = 0
        self.west = 0
        self.south = 0
        self.east = 0
        self.directions = {'n': [i for i in range(45, 135)],
                           'w': [i for i in range(135, 225)],
                           's': [i for i in range(225, 315)],
                           'e': [*[i for i in range(315, 360)], *[i for i in range(45)]]}

    def __call__(self, direction: str):
        exec(f"self.%s += 1" % direction)
        vertical = self.north - self.south
        horizontal = self.east - self.west
        if horizontal == 0:
            if vertical > 0:
                direction = 'n'
            elif vertical < 0:
                direction =  's'
        elif vertical == 0:
            if horizontal > 0:
                direction = 'e'
            elif horizontal < 0:
                direction = 'w'
        else:
            ans = math.atan2(vertical, horizontal) * (180 / math.pi)
            if ans < 0:
                ans += 360

            for key, value in self.directions.items():
                if int(ans) in value:
                    direction = key

        if direction != self.last_direction or direction is None:
            self.last_direction = direction
            first = True
        else:
            first = False
        return print_direction(direction, first)


def print_direction(direction: str, first: bool):
    """Frequency of landscapes determine probability"""
    north_choices = [Landscapes.mountain, Landscapes.blocked_mountain,
                     Landscapes.blocked_mountain, Landscapes.blocked_mountain]
    west_choices = None
    south_choices = None
    east_choices = None
    directions = {'n': north_choices, 'w': west_choices, 's': south_choices, 'e': east_choices}
    first_direction = {'n': Landscapes.mountain_range, 'w': None, 's': None, 'e': None}

    if not first:
        direction = directions[direction]
        selection = direction[random.randint(1, len(direction)) - 1]
    else:
        selection = first_direction[direction]
    return selection


def start_game():
    move = Displacement()
    print(Landscapes.main_village)
    print("You start your adventure in the village")
    choice = input("Which direction would you like to go?\n").lower()
    while choice not in ["north", "south", "east", "west", "nowhere"]:
        choice = input("Invalid direction (north, south, east, west)\n").lower()
    lazy_choices = ["You decide to take a nap", "You sit down and start playing with the grass",
                    "Someone hits you in the head with a rock", "Your neighbor reports you for soliciting"]
    if choice == "nowhere":
        print(lazy_choices[random.randint(1, 4) - 1])
        time.sleep(.5)
        return main_menu()
    else:
        alive = True

    while alive:
        print(move(choice))
        time.sleep(.5)
        choice = input("Which direction would you like to go?\n").lower()
        while choice not in ["north", "south", "east", "west"]:
            choice = input("Invalid direction (north, south, east, west)\n").lower()