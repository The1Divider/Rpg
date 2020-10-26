from Sprites import *
from InventorySystem import *
from Game import start_game
inv = Inventory()


def start_menu():
    print(Menus.start_menu)
    while True:
        selection = input(">").lower()
        if selection in ["1", "new game"]:
            inv.new_player()
            main_menu()
        elif selection in ["2", "load game"]:
            inv.load_player()
            main_menu()
        elif selection in ["3", "help"]:
            break
        elif selection in ["4", "quit", "exit", "stop"]:
            quit()
        else:
            print("Invalid selection")


def main_menu():
    print(Menus.main_menu)
    while True:
        selection = input(">").lower()
        if selection in ["1", "quest"]:
            start_game()
            print(Menus.main_menu)
        elif selection in ["2", "inventory"]:
            return inventory_display()
        elif selection in ["3", "shop"]:
            break
        elif selection in ["4", "stats"]:
            break
        elif selection in ["5", "load", "save"]:
            if selection == "5":
                selection = input("Load or save a character file?:\n").lower()
            if selection == "save":
                inv.save_player()
            elif selection == "load":
                inv.load_player()
            print(Menus.main_menu)
        elif selection in ["6", "exit", "quit", "stop"]:
            quit()
        else:
            print("Invalid selection")


def inventory_display():
    inv.inventory_setup()
    a, w, b = inv.armour_list_temp, inv.weapon_list_temp, inv.bag_list_temp
    armour = Menus.InventoryMenus.inventory_armour_menu(a)
    weapon = Menus.InventoryMenus.inventory_weapon_menu(w)
    bag = Menus.InventoryMenus.inventory_bag_menu(b)
    del inv.armour_list_temp, inv.weapon_list_temp, inv.bag_list_temp, a, w, b

    def armour_menu():
        print(armour)
        selection = None
        while selection not in [1, 2, 3]:
            try:
                selection = int(input("1) Select Item, 2) Next Page, 3) Exit\n"))
                if selection in [1, 2, 3]:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid Selection")

        if selection == 1:
            pass
        elif selection == 2:
            return weapon_menu()
        elif selection == 3:
            return main_menu()

    def weapon_menu():
        print(weapon)
        while True:
            try:
                selection = int(input("1) Select Item, 2) Next Page 3) Previous Page, 4) Exit\n"))
                if selection in [1, 2, 3, 4]:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid Selection")

        if selection == 1:
            pass
        elif selection == 2:
            return bag_menu()
        elif selection == 3:
            return armour_menu()
        elif selection == 4:
            return main_menu()

    def bag_menu():
        print(bag)
        selection = None
        while selection not in [1, 2, 3]:
            try:
                selection = int(input("1) Select Item, 2) Previous Page, 3) Exit\n"))
                if selection in [1, 2, 3]:
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Invalid Selection")

        if selection == 1:
            return main_menu()
        elif selection == 2:
            return weapon_menu()
        elif selection == 3:
            return main_menu()
    armour_menu()


if __name__ == "__main__":
    start_menu()
