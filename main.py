from Game import *
from Objects.Sprites import MenuSprites, MenuType, InventoryDisplayType

inv = Inventory()
exit_list = ["quit", "exit", "stop", "end"]


def start_menu() -> Optional[MenuType]:
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

    with suppress(ValueError):
        selection = int(selection)

    if type(selection) != int:
        selection = selection.lower()

    if selection in [1, "new game"]:
        inv.new_player()
        return main_menu()

    elif selection in [2, "load game"]:
        inv.load_player()
        return main_menu()

    elif selection in [3, "help"]:
        pass

    elif selection in [4, *exit_list]:
        quit()


def main_menu() -> Optional[Union[MenuType, InventoryDisplayType]]:
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
        inventory_display(_inv=inv)
        return main_menu()

    elif selection in [3, "shop"]:
        pass

    elif selection in [4, "stats"]:
        return stats_display(_inv=inv)

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


def inventory_display(_inv: Inventory) -> None:
    """Displays with setup"""
    _inv.inventory_setup()
    a, w, b = _inv.armour_list_temp, _inv.weapon_list_temp, _inv.bag_list_temp
    armours = MenuSprites.InventoryMenus.inventory_armour_menu(a)
    weapons = MenuSprites.InventoryMenus.inventory_weapon_menu(w)
    bag = MenuSprites.InventoryMenus.inventory_bag_menu(b)
    del a, w, b
    _inv.armour_list_temp, _inv.weapon_list_temp, _inv.bag_list_temp = [], [], []

    def armour_menu() -> MenuType:
        """Display for armour"""
        input_message = "1) Select Item, 2) Next Page, 3) Exit\n"
        print(armours)
        while (selection := input(input_message)) not in ("1", "2", "3"):
            print(f"Invalid Selection: {selection}")
        if selection == "1":
            armour_selection = input("Selection: ").lower()
            armour_selection_list = ("helmet", "chestplate", "leggings", "boots", "ring1", "ring2")

            if armour_selection in ("ring 1", "ring 2"):
                armour_selection = armour_selection.replace(" ", "")

            if armour_selection in armour_selection_list:
                print(MenuSprites.InventoryMenus.armour_selection(getattr(inv.Armour, armour_selection)))

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
                        print(MenuSprites.InventoryMenus.armour_selection(item[1]))

            return armour_menu()

        elif selection == "2":
            return weapon_menu()

        elif selection == "3":
            inv.bag_list_temp = []
            return main_menu()

    def weapon_menu() -> MenuType:
        """Display for weapon slots + quiver"""
        input_message = "1) Select Item, 2) Next Page 3) Previous Page, 4) Exit\n"
        print(weapons)

        while (selection := input(input_message)) not in ("1", "2", "3", "4"):
            print("Invalid Selection")

        if selection == "1":
            weapon_selection = input("Selection: ").lower()

            if weapon_selection in ("weapon 1", "weapon 2"):
                weapon_selection = weapon_selection.replace(" ", "")

            if weapon_selection in ("weapon1", "weapon2"):
                print(MenuSprites.InventoryMenus.weapon_selection(getattr(inv.Weapons, weapon_selection)))
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
                        print(MenuSprites.InventoryMenus.weapon_selection(item[1]))

                else:
                    print("Invalid Selection")

            return weapon_menu()

        elif selection == "2":
            return bag_menu()

        elif selection == "3":
            return armour_menu()

        elif selection == "4":
            return main_menu()

    def bag_menu() -> Optional[MenuType]:
        input_message = "1) Select Item, 2) Equip Weapon, 3) Previous Page, 4) Exit\n"
        print(bag)

        while (selection := input(input_message)) not in ("1", "2", "3", "4"):
            print("Invalid Selection")

        if selection == "1":

            weapon_selection = input("Selection: ").lower().replace(" ", "_")
            item = inv.get_item(weapon_selection)

            if item is not None and item != -1:
                menu = MenuSprites.InventoryMenus.weapon_selection(item)
                print(menu)

            elif item is None:
                print("There's nothing to select")

            elif item == -1:
                print("Invalid selection")

            return bag_menu()

        elif selection == "2":
            weapon = input("Which weapon would you like to equip?\n").lower()
            inv.equip_weapon(weapon)
            return inventory_display(_inv=_inv)

        elif selection == "3":
            return weapon_menu()

        elif selection == "4":
            inv.bag_list_temp = []
            return main_menu()

    armour_menu()


def stats_display(_inv: Inventory) -> MenuType:
    """Setup and display player stats + armour/weapon stats"""
    stats_list = _inv.stats_setup()
    stat_display = MenuSprites.InventoryMenus.stats_menu(stats_list)
    print(stat_display)
    return main_menu()


if __name__ == "__main__":
    start_menu()
