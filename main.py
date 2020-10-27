from Sprites import *
from InventorySystem import *
from Game import start_game
inv = Inventory(dev_mode=False)


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
        elif selection == "code":
            with open("DevCode.txt", 'r') as f:
                code = str(f.read())
            inp = input("Enter code")
            if inp == code:
                inv.dev_mode = True
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
            armour_selection = input("Selection: ").lower()
            armour_selection_list = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
            if armour_selection in ["ring 1", "ring 2"]:
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
            return armour_menu()
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
            weapon_selection = input("Selection: ").lower()
            if weapon_selection in ["weapon 1, weapon 2"]:
                weapon_selection = weapon_selection.replace(" ", "")
            if weapon_selection in ["weapon1", "weapon2"]:
                print(Menus.InventoryMenus.weapon_selection(getattr(inv.Weapons, weapon_selection)))
                return weapon_menu()
            else:
                weapon_selection = weapon_selection.title()
                weapon_list = [getattr(inv.Weapons, attribute) for attribute in ["weapon1", "weapon2"]]
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
            # to do: all items in bag should(?) be weapons
            return main_menu()
        elif selection == 2:
            return weapon_menu()
        elif selection == 3:
            return main_menu()
    armour_menu()


if __name__ == "__main__":
    start_menu()
