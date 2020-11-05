import random
import math
import time
from dataclasses import dataclass

from Sprites import *


@dataclass
class Enemy:
    def __init__(self):
        self.name = "Rat"
        self.hp = 5
        self.dmg = 1
        self.defence = 0
        self.block = 0
# Move to Sprites or create new file (new dir with sprites + enemies + items?)

class Displacement:
    def __init__(self):
        self.last_direction = None
        self.north = 0
        self.west = 0
        self.south = 0
        self.east = 0
        self.village = None
        self.directions = {'n': [i for i in range(45, 135)],
                           'w': [i for i in range(135, 225)],
                           's': [i for i in range(225, 315)],
                           'e': [*[i for i in range(315, 360)], *[i for i in range(45)]]}

    def __call__(self, direction: str):
        """return new displacement of player based on past """
        exec(f"self.{direction} += 1")
        vertical = self.north - self.south
        horizontal = self.east - self.west
        if horizontal + vertical == 0:
            return self.village
        elif horizontal == 0:
            if vertical > 0:
                direction = 'n'
            elif vertical < 0:
                direction = 's'
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
    """Prints the landscape the player encounters based on which biome (direction) they're in
        Frequency of landscapes determine probability"""
    north_choices = [Landscapes.mountain, Landscapes.blocked_mountain,
                     Landscapes.blocked_mountain, Landscapes.blocked_mountain]
    west_choices = None
    south_choices = None
    east_choices = None
    directions = {'n': north_choices, 'w': west_choices, 's': south_choices, 'e': east_choices}
    first_direction = {'n': Landscapes.mountain_range, 'w': None, 's': None, 'e': None}

    if first:
        selection = first_direction[direction]
    else:
        direction = directions[direction]
        selection = direction[random.randint(1, len(direction)) - 1]
    return selection


class Encounter:
    def __init__(self, stats, weapons, armour, levels):
        self.enemy_alive, self.player_alive = True, True
        self.armour_slots = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
        self.weapon_slots = ["weapon1", "weapon2", "quiver"]
        self.stats, self.weapons, self.armour, self.levels = stats, weapons, armour, levels
        self.en = Enemy()
        self.stats_setup()
        self.main_loop()

    def main_loop(self):
        """Main encounter loop, runs through each encounter until either enemy/player hp hits 0"""
        while self.enemy_alive and self.player_alive:
            player_dmg, player_blocked = self.player_turn()
            enemy_dmg, enemy_blocked = self.enemy_turn(player_blocked)
            if enemy_blocked:
                player_dmg = 0
            self.en.hp -= player_dmg
            print(f"You dealt {player_dmg} Dmg") if player_dmg != 0 else print(f"{self.en.name} blocked your attack")
            if self.en.hp <= 0:
                self.enemy_alive = False
            self.stats.hp -= enemy_dmg
            print(f"{self.en.name} dealt {enemy_dmg} Dmg to you") if enemy_dmg != 0 else print(f"You blocked the attack")
            if self.stats.hp <= 0:
                self.player_alive = False

        if self.player_alive:
            print("You win")
        elif self.enemy_alive:
            print("You lose")
        else:
            print("You killed each other??")

    def player_turn(self) -> (int, bool):
        """returns dmg player dealt + if they blocked the attack"""
        player_blocked = False
        selection = input("1) Attack 2) Defend 3) Inventory 4) Flee\n")
        while True:
            if selection == "1":
                player_damage = self.stats.dmg - self.en.defence if self.stats.dmg - self.en.defence >= 1 else 1
                if self.en.block != 0:
                    if self.en.block == random.randint(self.en.block, 100):
                        player_damage = 0
                return player_damage, player_blocked
            elif selection == "2":
                player_blocked = True if random.randint(-1, self.stats.block) else False
                player_damage = 0
                return player_damage, player_blocked
            elif selection == "3":
                pass
            elif selection == "4":
                pass
            else:
                print("Invalid input")

    def enemy_turn(self, player_blocked: bool) -> (int, bool):
        """returns dmg enemy dealt (in result of if the player blocked) + if they blocked"""
        enemy_damage = 0
        enemy_blocked = False
        if not player_blocked:
            if 1 == random.randint(1, 4):
                enemy_blocked = True
            else:
                enemy_damage = self.en.dmg - self.stats.defence if self.en.dmg - self.stats.defence >= 1 else 1
        return enemy_damage, enemy_blocked

    def stats_setup(self):
        """add together base stats + what's provided by weapons/armour"""
        for weapon in [getattr(self.weapons, attribute) for attribute in self.weapon_slots]:
            try:
                self.stats.dmg += weapon.dmg
                self.stats.crit += weapon.crit
            except AttributeError:
                pass
        for armour in [getattr(self.armour, attribute) for attribute in self.armour_slots]:
            try:
                self.stats.hp += armour.hp
                self.stats.defence += armour.defence
            except AttributeError:
                pass


def start_game(stats, weapons, armour, levels):
    """Main game loop: moves + provides encounters to the player based on levels + which biome they're in """
    Encounter(stats, weapons, armour, levels)
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
        return
    else:
        alive = True

    while alive:
        moved = move(choice)
        if moved is None:
            print("You've returned to the village")
            return
        else:
            print(moved)
        time.sleep(.5)
        choice = input("Which direction would you like to go?\n").lower()
        while choice not in ["north", "south", "east", "west"]:
            choice = input("Invalid direction (north, south, east, west)\n").lower()
