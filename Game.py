import math
import random

from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple

from InventorySystem import *
from Objects.Sprites import LandscapeSprites
from Objects.Enemies import *

SCALE = 10

class Error(Exception): pass
class InvalidDirection(Error): pass

class Displacement:
    def __init__(self) -> None:
        self.last_direction: Optional[str] = None
        self.x: int = 0
        self.y: int = 0
        self.directions: Dict = {'north': (0, 1),
                                 'west': (1, 0),
                                 'south': (0, -1),
                                 'east': (-1, 0)}

    def __call__(self, direction: str) -> Tuple[str, bool]:
        """return new displacement of player based on past """
        try:
            dx, dy = self.directions[direction]

        except KeyError:
            raise InvalidDirection

        self.x += dx
        self.y += dy

        if self.x > self.y and self.x > 0:
            direction = "west"

        elif self.x > self.y and self.x < 0:
            direction = "east"

        elif self.x < self.y and self.y > 0:
            direction = "north"

        elif self.x < self.y and self.y < 0:
            direction = "south"

        elif self.x == 0 and self.y == 0:
            direction = "returned"

        if direction != self.last_direction:
            self.last_direction = direction
            first = True
        
        else:
            first = False

        return direction, first

def print_direction(direction: str, first: bool) -> str:
    """Prints the landscape the player encounters based on which biome (direction) they're in
        Frequency of landscapes determine probability"""
    lan = LandscapeSprites
    north_choices = [lan.mountain, lan.mountain_blocked,
                     lan.mountain_blocked, lan.mountain_blocked]
    west_choices = [lan.tree1, lan.tree2]
    south_choices = ["No display"]
    east_choices = ["No display"]
    directions: Dict[str] = {"north": north_choices,
                             "west": west_choices,
                             "south": south_choices,
                             "east": east_choices}
    first_direction = {"north": lan.mountain_range,
                       "west": lan.forest,
                       "south": "No first display",
                       "east": "No first display"}

    if first:
        selection = first_direction[direction]

    else:
        player_direction = directions[direction]
        selection = player_direction[random.randint(1, len(player_direction)) - 1]

    return selection


@dataclass
class Stats:
    player_hp: int
    player_armour_hp: int
    player_dmg: int
    player_weapon_dmg: int
    player_defence: int
    player_armour_defence: int
    player_crit: int
    player_weapon_crit: int
    player_crit_chance: int
    player_weapon_crit_chance: int
    player_block: int
    player_player_level: int
    player_exp: int
    player_exp_percent: int
    player_current_hp: int


class Encounter(Stats):
    def __init__(self, _inv: Inventory, enemy: Any) -> None:
        self.inv, self.en = _inv, enemy
        self.enemy_alive, self.player_alive = True, True
        self.exp_gain = 0

        stats_list, current_hp = self.inv.display.stats_setup(in_loop=True)
        super().__init__(*stats_list, current_hp)
        self.enemy_setup(self.en)

        self.main_loop()

    def main_loop(self) -> None:
        self.exp_gain = self.en.hp * 10
        """Main encounter loop, runs through each encounter until either enemy/player hp hits 0"""
        print(self.en.passive_sprite)

        while self.enemy_alive and self.player_alive:
            player_dmg, player_blocked = self.player_turn()
            enemy_dmg, enemy_blocked = self.enemy_turn(player_blocked)

            if enemy_blocked:
                player_dmg = 0

            self.en.hp -= player_dmg
            print(f"You dealt {player_dmg} Dmg" if player_dmg != 0 else f"{self.en.name} blocked your attack")

            if self.en.hp <= 0:
                self.enemy_alive = False

            self.player_current_hp -= enemy_dmg
            print(f"{self.en.name} dealt {enemy_dmg} Dmg to you" if enemy_dmg != 0 else f"You blocked the attack")

            if self.player_current_hp <= 0:
                self.player_alive = False

            print(self.en.aggro_sprite)

        if self.player_alive:
            print("You win")

        elif self.enemy_alive:
            print("You lose")
            self.exp_gain = 0

        else:
            print("You killed each other???")
            self.exp_gain = 0

        return None

    def enemy_setup(self, en: Any) -> None:
        """Setup enemy stats based on enemy level which in turn is based on player level"""
        player_level = self.inv.state.Levels.player_level
        en.level = player_level if player_level <= self.en.level_cap else self.en.level_cap
        en.hp *= self.en.level
        en.dmg *= self.en.level
        en.defence *= self.en.level
        en.block *= self.en.level

    def player_turn(self) -> Tuple[int, bool]:
        """returns dmg player dealt + if they blocked the attack"""
        player_blocked = False
        input_message = "1) Attack 2) Defend 3) Inventory 4) Flee\n"

        while True:
            while (selection := input(input_message).lower()) not in \
                    ("1", "attack", "2", "defend", "3", "inventory", "4" "flee"):
                print("Invalid Input")

            if selection == "1":
                player_damage = self.player_dmg - self.en.defence if self.player_dmg - self.en.defence >= 1 else 1

                if random.randint(1, 100) in range(1, self.player_crit_chance + 1):
                    player_damage += self.player_crit

                if self.en.block != 0:
                    if random.randint(1, 100) in range(1, self.en.block + 1):
                        player_damage = 0

                return player_damage, player_blocked

            elif selection == "2":
                player_blocked = True if random.randint(0, self.player_block) == 0 else False
                player_damage = 0
                return player_damage, player_blocked

            elif selection == "3":
                pass

            elif selection == "4":
                pass

            else:
                print("Invalid input")

    def enemy_turn(self, player_blocked: bool) -> Tuple[int, bool]:
        """returns dmg enemy dealt (in result of if the player blocked) + if they blocked"""
        enemy_damage = 0
        enemy_blocked = False

        if not player_blocked:

            if self.en.block != 0 and random.randint(0, self.en.block) == 0:
                enemy_blocked = True

            else:
                enemy_damage = self.en.dmg - self.player_defence if self.en.dmg - self.player_defence >= 1 else 1

        return enemy_damage, enemy_blocked


def encounter_xy_sigmoid(distance_x: int, distance_y: int) -> int:
    """Calculates the chance of having an encounter \n
       Based on the sigmoid function:
        - closer to (0,0) = low encounter chance
        - ~60 displacement = 99% encounter chance"""
    total_chance = 0
    for distance in (distance_x, distance_y):
        total_chance += round(abs((1 / (1 + math.e ** -(distance / SCALE)) - 0.5) * 200))
    return total_chance // 2


def start_game(_inv: Inventory) -> None:
    """Main game loop: moves + provides encounters to the player based on levels + which biome they're in """
    move = Displacement()
    _inv.state.Stats.__post_init__()
    print(LandscapeSprites.main_village)
    choice_message = "Which direction would you like to go?\n"

    while (choice := input(choice_message).lower()) not in ["north", "south", "east", "west", "nowhere"]:
        print("Invalid direction (north, south, east, west)\n")

    lazy_choices = ["You decide to take a nap", "You sit down and start playing with the grass",
                    "Someone hits you in the head with a rock", "Your neighbor reports you for soliciting"]

    if choice == "nowhere":
        print(lazy_choices[random.randint(0, 3)])
        return None

    else:
        alive = True

    while alive:
        try:
            moved, first = move(choice)

            if moved == "returned":
                print("You've returned to the village")
                return None
                
            print(print_direction(moved, first))

        except InvalidDirection:
            print(f"Invalid direction: {choice}")
            choice = input(choice_message).lower()
            continue

        encounter_chance = encounter_xy_sigmoid(abs(move.x), abs(move.y))

        if random.randint(1, 100) in range(encounter_chance):
            encounter = Encounter(_inv, enemy=Rat())
            current_hp, alive, exp_gain = encounter.player_current_hp, encounter.player_alive, encounter.exp_gain
            setattr(_inv.state.Stats, "current_hp", current_hp)
            total_exp = getattr(_inv.state.Levels, "player_exp")
            setattr(_inv.state.Levels, "player_exp", total_exp + exp_gain)

            if not alive:
                continue

        else:
            choice = input(choice_message)
