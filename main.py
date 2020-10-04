import random
import json
from Landscapes import *

global character, character_save, level

class MainMenu:
    def __init__(self):
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
                load_save_selection = input("Load or save a character file?:\n")
                loadSave(load_save_selection)
                return MainMenu()
            elif selection in ["6", "exit", "quit", "stop"]:
                quit()
            else:
                print("Invalid selection")


def loadSave(selection):
    if selection == "save":
        with open("character.json", "w") as f:
            player_save = {
                "Is_Save": False
                "Character": {
                    "Items": None,
                    "Balance": None,
                    "Stats": None
                },
                "Level": {
                    "Difficulty": None,
                    "Enemy_and_Player": {
                        "Player": None,
                        "Enemy": None
                    }
                }
            }
            json.dump(player_save, f, indent=2)
            print("Success!")

    elif selection == "load":
        with open("character.json", "r") as f:
            player_save = json.load(f)
            character = player_save["Character"]
            character_save = player_save["Is_Save"]
            level = player_save["Level"]
            from InventorySystem import InventorySys
            InventorySys(character, character_save)
            print("Success!")


if __name__ == "__main__":
    print(help(json.dump))
    MainMenu()
