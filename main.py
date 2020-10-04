import random
import json
from Landscapes import *
from InventorySystem import *

global character, character_save, level


def startMenu():
    print(Menus.start_menu)
    while True:
        selection = input(">").lower()
        if selection in ["1", "new game"]:
            character_save = False
            character = newPlayer()
            mainMenu(character)
        elif selection in ["2", "load game"]:
            break
        elif selection in ["3", "help"]:
            break
        elif selection in ["4", "quit", "exit", "stop"]:
            quit()


def mainMenu(character):
    print(Menus.main_menu)
    while True:
        selection = input(">").lower()
        if selection in ["1", "quest"]:
            break
        elif selection in ["2", "inventory"]:
            break
        elif selection in ["3", "shop"]:
            break
        elif selection in ["4", "stats"]:
            break
        elif selection in ["5", "load", "save"]:
            load_save_selection = input("Load or save a character file?:\n").lower()
            loadSave(load_save_selection, character)
            return mainMenu()
        elif selection in ["6", "exit", "quit", "stop"]:
            quit()
        else:
            print("Invalid selection")


def loadSave(selection, player):
    if selection == "save":
        with open("../../Documents/GitHub/Rpg/character.json", "w") as f:
            json.dump(player, f, indent=2)
            print("Success!")

    elif selection == "load":
        with open("../../Documents/GitHub/Rpg/character.json", "r") as f:
            player_save = json.load(f)
            character = player_save["Character"]
            character_save = player_save["Is_Save"]
            level = player_save["Level"]
            from InventorySystem import Inventory
            Inventory(character_save, character)
            print("Success!")


if __name__ == "__main__":
    startMenu()
