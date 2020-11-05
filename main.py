from contextlib import suppress
from Sprites import *
from InventorySystem import *
from Game import *

inv = Inventory()


def start_menu():
    option_list = ("1", "new game", "2", "load game", "3", "help", "4", "quit", "exit", "stop", "end")
    print(Menus.start_menu)
    while (selection := input(">")) not in option_list:
        print(f"Invalid selection: {selection}")
    if type(selection) != int:
        selection = selection.lower()
    if selection in option_list[0:2]:
        inv.new_player()
        return main_menu()
    elif selection in option_list[2:4]:
        inv.load_player()
        return main_menu()
    elif selection in option_list[4:6]:
        pass
    elif selection in option_list[6:]:
        quit()


def main_menu():
    option_list = ("1", "quest", "2", "inventory", "3", "shop", "4", "stats", "5", "load", "save",
                   "6", "quit", "stop", "end", "exit", "code")
    print(Menus.main_menu)
    while (selection := input(">")) not in option_list:
        print(f"Invalid selection: {selection}")
    if type(selection) != int:
        selection = selection.lower()

    if selection in option_list[0:2]:
        start_game(inv.Stats, inv.Weapons, inv.Armour, inv.Levels)
        return main_menu()
    elif selection in option_list[2:4]:
        inventory_display()
        return main_menu()
    elif selection in option_list[4:6]:
        pass
    elif selection in option_list[6:8]:
        pass
    elif selection in option_list[8:11]:
        if selection == "5":
            while selection := input("Load or save a character file?:\n").lower() not in ("save", "load"):
                print("Invalid selection")
        if selection == "save":
            inv.save_player()
        elif selection == "load":
            inv.load_player()
        return main_menu()
    elif selection in option_list[11:16]:
        quit()
    elif selection == option_list[16]:
        with open("DevCode.txt", 'r') as f:
            code = str(f.read())
        inp = input("Enter code")
        if inp == code:
            inv.dev_mode = True
        return main_menu()


def inventory_display():
    inv.inventory_setup()
    a, w, b = inv.armour_list_temp, inv.weapon_list_temp, inv.bag_list_temp
    armour = Menus.InventoryMenus.inventory_armour_menu(a)
    weapon = Menus.InventoryMenus.inventory_weapon_menu(w)
    bag = Menus.InventoryMenus.inventory_bag_menu(b)
    del a, w, b
    inv.armour_list_temp, inv.weapon_list_temp, inv.bag_list_temp = [], [], []

    def armour_menu():
        input_message = "1) Select Item, 2) Next Page, 3) Exit\n"
        print(armour)
        while (selection := input(input_message)) not in ("1", "2", "3"):
            print(f"Invalid Selection: {selection}")
        if selection == "1":
            armour_selection = input("Selection: ").lower()
            armour_selection_list = ("helmet", "chestplate", "leggings", "boots", "ring1", "ring2")
            if armour_selection in ("ring 1", "ring 2"):
                armour_selection = armour_selection.replace(" ", "")
            if armour_selection in armour_selection_list:
                print(Menus.InventoryMenus.armour_selection(getattr(inv.Armour, armour_selection)))
            else:
                armour_selection = armour_selection.title()
                armour_list = [getattr(inv.Armour, attribute) for attribute in armour_selection_list]
                for item in armour_list:
                    try:
                        armour_list[armour_list.index(item)] = (item.name, item)
                    except AttributeError:
                        armour_list[armour_list.index(item)] = (None, item)
                for item in armour_list:
                    if item[0] == armour_selection:
                        print(Menus.InventoryMenus.armour_selection(item[1]))
            armour_menu()
        elif selection == "2":
            return weapon_menu()
        elif selection == "3":
            return main_menu()

    def weapon_menu():
        input_message = "1) Select Item, 2) Next Page 3) Previous Page, 4) Exit\n"
        print(weapon)
        while (selection := input(input_message)) not in ("1", "2", "3", "4"):
            print("Invalid Selection")

        if selection == "1":
            weapon_selection = input("Selection: ").lower()
            if weapon_selection in ("weapon 1, weapon 2"):
                weapon_selection = weapon_selection.replace(" ", "")
            if weapon_selection in ("weapon1", "weapon2"):
                print(Menus.InventoryMenus.weapon_selection(getattr(inv.Weapons, weapon_selection)))
                return weapon_menu()
            else:
                weapon_selection = weapon_selection.title()
                weapon_list = [getattr(inv.Weapons, attribute) for attribute in ("weapon1", "weapon2")]
                for item in weapon_list:
                    try:
                        weapon_list[weapon_list.index(item)] = (item.name, item)
                    except AttributeError:
                        weapon_list[weapon_list.index(item)] = (None, item)
                for item in weapon_list:
                    if item[0] == weapon_selection:
                        print(Menus.InventoryMenus.weapon_selection(item[1]))
                else:
                    print("Invalid Selection")
            return weapon_menu()

        elif selection == "2":
            return bag_menu()
        elif selection == "3":
            return armour_menu()
        elif selection == "4":
            return main_menu()

    def bag_menu():
        input_message = "1) Select Item, 2) Previous Page, 3) Exit\n"
        print(bag)
        while (selection := input(input_message)) not in ("1", "2", "3"):
            print("Invalid Selection")

        if selection == "1":
            # to do: all items in bag should(?) be weapons
            return main_menu()
        elif selection == "2":
            return weapon_menu()
        elif selection == "3":
            return main_menu()
    armour_menu()


if __name__ == "__main__":
    start_menu()
