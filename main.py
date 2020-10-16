import random
import time
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
            startGame()

        elif selection in ["2", "inventory"]:
            inventoryDisplay()
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


def inventoryDisplay():
    armour_list, weapon_list, bag_list = Inventory.inventorySetup(inventory)
    armour = Menus.InventoryMenus.inventoryArmourMenu(armour_list[0][1].name, armour_list[1][1].name,
                                                      armour_list[2][1].name, armour_list[3][1].name,
                                                      armour_list[4][1].name, armour_list[5][1].name)
    weapon = Menus.InventoryMenus.inventoryWeaponMenu(weapon_list[0][1].name, weapon_list[1][1].name,
                                                      weapon_list[2][1].name)
    bag = Menus.InventoryMenus.inventoryBagMenu(bag_list[0], bag_list[1], bag_list[2], bag_list[3], bag_list[4],
                                                bag_list[5], bag_list[6], bag_list[7], bag_list[8], bag_list[9])

    def armour_menu():
        print(armour)
        selection = None
        while selection not in [1, 2, 3]:
            try:
                selection = int(input("1) Select Item, 2) Next Page, 3) Exit\n"))
                if selection not in [1, 2, 3]:
                    print("Invalid Selection")
                    selection = input("1) Select Item, 2) Next Page, 3) Exit\n")
                else:
                    break
            except ValueError:
                print("Invalid Selection")
                selection = input("1) Select Item, 2) Next Page, 3) Exit\n")

        if selection == 1:
            pass
        elif selection == 2:
            return weapon_menu()
        elif selection == 3:
            return mainMenu()

    def weapon_menu():
        print(weapon)
        selection = None
        while True:
            try:
                selection = int(input("1) Select Item, 2) Next Page 3) Previous Page, 4) Exit\n"))
                if selection not in [1, 2, 3, 4]:
                    print("Invalid Selection")
                    selection = input("1) Select Item, 2) Next Page, 3) Previous Page, 4) Exit\n")
                else:
                    break
            except ValueError:
                print("Invalid Selection")
                selection = input("1) Select Item, 2) Next Page, 3) Previous Page, 4) Exit\n")

        if selection == 1:
            pass
        elif selection == 2:
            return bag_menu()
        elif selection == 3:
            return armour_menu()
        elif selection == 4:
            return mainMenu()

    def bag_menu():
        print(bag)
        selection = None
        while selection not in [1, 2, 3]:
            try:
                selection = int(input("1) Select Item, 2) Previous Page, 3) Exit\n"))
                if selection not in [1, 2, 3]:
                    print("Invalid Selection")
                    selection = input("1) Select Item, 2) Previous Page, 3) Exit\n")
                else:
                    break
            except ValueError:
                print("Invalid Selection")
                selection = input("1) Select Item, 2) Previous Page, 3) Exit\n")

        if selection == 1:
            pass
        elif selection == 2:
            return weapon_menu()
        elif selection == 3:
            return mainMenu()

    armour_menu()



def startGame():
    print(Landscapes.main_village)
    print("You start your adventure in the village")
    start_choice = input("Which direction would you like to go?\n").lower()
    while start_choice not in ["north", "south", "east", "west", "nowhere"]:
        start_choice = input("Invalid direction (north, south, east, west)\n")

    if start_choice == "nowhere":
        lazy_selection = random.randint(1,4)
        if lazy_selection == 1:
            print("You decide to take a nap")
        elif lazy_selection == 2:
            print("You sit down and start playing with the grass")
        elif lazy_selection == 3:
            print("Someone hits you in the head with a rock")
        elif lazy_selection == 4:
            print("Your neighbor reports you for soliciting")
        time.sleep(.5)
        mainMenu()


if __name__ == "__main__":
    startMenu()
