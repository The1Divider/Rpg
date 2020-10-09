from Sprites import *
from InventorySystem import *
global inventory


def startMenu():
    print(Menus.start_menu)
    while True:
        selection = input(">").lower()
        if selection in ["1", "new game"]:
            global inventory
            inventory = Inventory(None, new_player=True)
            return mainMenu()

        elif selection in ["2", "load game"]:
            Inventory.loadPlayer()
            return mainMenu()

        elif selection in ["3", "help"]:
            break

        elif selection in ["4", "quit", "exit", "stop"]:
            quit()


def mainMenu():
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
            if selection == "5":
                selection = input("Load or save a character file?:\n").lower()

            if selection == "save":
                Inventory.savePlayer(inventory)

            elif selection == "load":
                Inventory.loadPlayer()

            print(Menus.main_menu)

        elif selection in ["6", "exit", "quit", "stop"]:
            quit()

        else:
            print("Invalid selection")


if __name__ == "__main__":
    startMenu()
