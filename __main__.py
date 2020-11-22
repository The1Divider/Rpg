from typing import Optional, Union
from contextlib import suppress

from .Game import start_game
from .Objects.Sprites import MenuSprites, MenuType, InventoryDisplayType
from .InventorySystem import PlayerInv

inv = PlayerInv()
exit_list = ["quit", "exit", "stop", "end"]


def start_menu() -> None:
    """Start menu of the game
       Contains access to:
        - Opening a game:
            - A new game
            - Loading a previous save file
        - Help menu (todo)"""
    option_list = ("1", "new game", "2", "load game", "3", "help", "4", *exit_list)
    print(MenuSprites.start_menu)

    while (selection := input(">").lower()) not in option_list:
        print(f"Invalid selection: {selection}")

    selection = selection.lower()

    if selection in ["1", "new game"]:
        inv.new_player()
        return main_menu()

    elif selection in ["2", "load game"]:
        inv.load_player()
        return main_menu()

    elif selection in ["3", "help"]:
        pass

    elif selection in ["4", *exit_list]:
        quit()


def main_menu() -> None:
    """Main menu of the game
       Contains access to:
        - Main loop
        - Inventory + Stats displays
        - Shop (todo)
        - Saving + Loading
        """
    option_list = ("1", "quest", "2", "inventory", "3", "shop", "4", "stats", "5", "load", "save",
                   "6", *exit_list, "code")

    print(MenuSprites.main_menu)

    while (selection := input(">").lower()) not in option_list:
        print(f"Invalid selection: {selection}")

    with suppress(ValueError):
        selection = int(selection)

    if selection in [1, "quest"]:
        start_game(_inv=inv)
        return main_menu()

    elif selection in [2, "inventory"]:
        inv.InventoryDisplay.inventory_display()
        return main_menu()

    elif selection in [3, "shop"]:
        pass

    elif selection in [4, "stats"]:
        inv.InventoryDisplay.stats_display(in_loop=False)
        return main_menu()

    elif selection in [5, "save", "load"]:

        if selection not in ["save", "load"]:
            while selection := input("Load or save a character file?:\n").lower() not in ("save", "load"):
                print("Invalid selection")

        if selection == "save":
            inv.save_player()
            return main_menu()

        elif selection == "load":
            inv.load_player()
            return main_menu()

    elif selection in [6, *exit_list]:
        quit()

    elif selection == "code":
        with open("DevCode.txt", 'r') as f:
            code = str(f.read())

        inp = input("Enter code")

        if inp == code:
            inv.dev_mode = True

        return main_menu()

start_menu()
