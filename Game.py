import random
import math
import time
from typing import Any

from InventorySystem import *
from Sprites import *

SCALE = 10


@dataclass
class Enemy:
    class Rat:
        def __init__(self) -> None:
            self.sprite = Enemies.rat_passive
            self.level = 1
            self.level_cap = 5
            self.name = "Rat"
            self.hp = 5
            self.dmg = 1
            self.defence = 0
            self.block = 0
# Move to Sprites or create new file (new dir with sprites + enemies + items?)


class Displacement:
    def __init__(self) -> None:
        self.last_direction = None
        self.north = 0
        self.west = 0
        self.south = 0
        self.east = 0
        self.directions = {'n': [i for i in range(45, 135)],
                           'w': [i for i in range(135, 225)],
                           's': [i for i in range(225, 315)],
                           'e': [*[i for i in range(315, 360)], *[i for i in range(45)]]}

    def __call__(self, direction: str) -> Optional[str]:
        """return new displacement of player based on past """
        setattr(self, direction, getattr(self, direction) + 1)
        self.vertical = self.north - self.south
        self.horizontal = self.east - self.west

        if self.horizontal + self.vertical == 0 and self.south - self.north == self.vertical \
                and self.west - self.east == self.horizontal:
            return None

        elif self.horizontal == 0 and not (self.north == 0 and self.south == 0):

            if self.vertical > 0:
                direction = 'n'

            elif self.vertical < 0:

                direction = 's'

        elif self.vertical == 0 and not (self.west == 0 and self.east == 0):

            if self.horizontal > 0:
                direction = 'e'

            elif self.horizontal < 0:
                direction = 'w'

        else:
            ans = math.atan2(self.vertical, self.horizontal) * (180 / math.pi)

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

    def average(self) -> tuple[int, int]:
        return abs(self.vertical), abs(self.horizontal)


def print_direction(direction: str, first: bool) -> str:
    """Prints the landscape the player encounters based on which biome (direction) they're in
        Frequency of landscapes determine probability"""
    lan = Landscapes
    north_choices = [lan.mountain, lan.mountain_blocked,
                     lan.mountain_blocked, lan.mountain_blocked]
    west_choices = [lan.tree1, lan.tree2]
    south_choices = None
    east_choices = None
    directions = {'n': north_choices, 'w': west_choices, 's': south_choices, 'e': east_choices}
    first_direction = {'n': lan.mountain_range, 'w': lan.forest, 's': None, 'e': None}

    if first:
        selection = first_direction[direction]

    else:
        direction = directions[direction]
        selection = direction[random.randint(1, len(direction)) - 1]

    return selection


class Encounter:
    def __init__(self, stats: Stats, weapons: Weapons, armour: Armour, levels: Levels, enemy: Any) -> None:
        self.enemy_alive, self.player_alive = True, True

        self.armour_slots = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
        self.weapon_slots = ["weapon1", "weapon2", "quiver"]
        self.stats, self.weapons, self.armour, self.levels = stats, weapons, armour, levels

        self.stats_setup()
        self.en = enemy()
        self.enemy_setup()

        self.main_loop()

    def main_loop(self) -> bool:
        """Main encounter loop, runs through each encounter until either enemy/player hp hits 0"""
        print(self.en.sprite)

        while self.enemy_alive and self.player_alive:
            player_dmg, player_blocked = self.player_turn()
            enemy_dmg, enemy_blocked = self.enemy_turn(player_blocked)

            if enemy_blocked:
                player_dmg = 0

            self.en.hp -= player_dmg
            print(f"You dealt {player_dmg} Dmg" if player_dmg != 0 else f"{self.en.name} blocked your attack")

            if self.en.hp <= 0:
                self.enemy_alive = False

            self.stats.hp -= enemy_dmg
            print(f"{self.en.name} dealt {enemy_dmg} Dmg to you" if enemy_dmg != 0 else f"You blocked the attack")

            if self.stats.hp <= 0:
                self.player_alive = False

        if self.player_alive:
            print("You win")

        elif self.enemy_alive:
            print("You lose")

        else:
            print("You killed each other???")

        return self.player_alive

    def enemy_setup(self) -> None:
        """Setup enemy stats based on enemy level which in turn is based on player level"""
        self.en.level = self.levels.player_level if self.levels.player_level <= self.en.level_cap else self.en.level_cap
        self.en.hp *= self.en.level
        self.en.dmg *= self.en.level
        self.en.defence *= self.en.level
        self.en.block *= self.en.level

    def player_turn(self) -> tuple[int, bool]:
        """returns dmg player dealt + if they blocked the attack"""
        player_blocked = False
        input_message = "1) Attack 2) Defend 3) Inventory 4) Flee\n"

        while True:
            while (selection := input(input_message).lower()) not in ("1", "attack", "2", "defend", "3", "inventory", "4" "flee"):
                print("Invalid Input")

            if selection == "1":
                player_damage = self.stats.dmg - self.en.defence if self.stats.dmg - self.en.defence >= 1 else 1

                if random.randint(1, 100) in random.randint(1, self.stats.crit_chance + 1):
                    player_damage += self.stats.crit

                if self.en.block != 0:
                    if random.randint(1, 100) in range(1, self.en.block + 1):
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

    def enemy_turn(self, player_blocked: bool) -> tuple[int, bool]:
        """returns dmg enemy dealt (in result of if the player blocked) + if they blocked"""
        enemy_damage = 0
        enemy_blocked = False
        if not player_blocked:
            if 1 == random.randint(1, 4):
                enemy_blocked = True

            else:
                enemy_damage = self.en.dmg - self.stats.defence if self.en.dmg - self.stats.defence >= 1 else 1
        return enemy_damage, enemy_blocked

    def stats_setup(self) -> None:
        """add together base stats + what's provided by weapons/armour"""
        # change for selected weapon slot
        for weapon in [getattr(self.weapons, attribute) for attribute in self.weapon_slots]:
            try:
                self.stats.dmg += weapon.dmg
                self.stats.crit += weapon.crit
                self.stats.crit_chance += weapon.crit_chance
            except AttributeError:
                pass
        for armour in [getattr(self.armour, attribute) for attribute in self.armour_slots]:
            try:
                self.stats.hp += armour.hp
                self.stats.defence += armour.defence
            except AttributeError:
                pass


def encounter_xy_sigmoid(distance_x: int, distance_y: int) -> int:
    """Calculates the chance of having an encounter
       Based on the sigmoid -> closer to (0,0) = low encounter chance
                               further (~60 displacement) = 99% encounter chance"""
    total_chance = 0
    for distance in (distance_x, distance_y):
        total_chance += round(abs((1 / (1 + math.e ** -(distance / SCALE)) - 0.5) * 200))
    return total_chance // 2


def start_game(stats: Stats, weapons: Weapons, armour: Armour, levels: Levels) -> None:
    """Main game loop: moves + provides encounters to the player based on levels + which biome they're in """
    move = Displacement()
    print(Landscapes.main_village)
    choice_message = "Which direction would you like to go?\n"

    while (choice := input(choice_message).lower()) not in ["north", "south", "east", "west", "nowhere"]:
        print("Invalid direction (north, south, east, west)\n")

    lazy_choices = ["You decide to take a nap", "You sit down and start playing with the grass",
                    "Someone hits you in the head with a rock", "Your neighbor reports you for soliciting"]

    if choice == "nowhere":
        print(lazy_choices[random.randint(1, 4) - 1])
        time.sleep(.5)
        return None

    else:
        alive = True

    while alive:
        moved = move(choice)
        distance_away_x, distance_away_y = move.average()
        encounter_chance = encounter_xy_sigmoid(distance_away_x, distance_away_y)

        if random.randint(1, 100) in range(encounter_chance):
            alive = Encounter(stats, weapons, armour, levels, enemy=Enemy.Rat)

        if moved is None:
            print("You've returned to the village")
            return None

        else:
            print(moved)

        time.sleep(.5)

        while(choice := input(choice_message).lower()) not in ["north", "south", "east", "west"]:
            print("Invalid direction (north, south, east, west)\n")
