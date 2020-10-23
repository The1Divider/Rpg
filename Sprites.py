class Menus:
    start_menu = "------------------\n" \
                 "    Epic RPG      \n" \
                 "------------------\n" \
                 "1) New Game       \n" \
                 "2) Load Game      \n" \
                 "3) Help           \n" \
                 "4) Quit             "

    main_menu = "------------------\n" \
                "    Main Menu     \n" \
                "------------------\n" \
                "1) Quest          \n" \
                "2) Inventory      \n" \
                "3) Shop           \n" \
                "4) Stats          \n" \
                "5) Load/Save      \n" \
                "6) Exit             "

    class InventoryMenus:
        @staticmethod
        def inventory_menu_spacing(menu_list, special_list):
            """Method to align inventory display regardless of item name size"""
            max_length = len(max(menu_list, key=len))
            for i in menu_list:
                ind = menu_list.index(i)
                if i in special_list:
                    while len(i) < max_length:
                        i = i[:-2] + "-" + i[-2:]
                        menu_list[ind] = i
                while len(i) < max_length:
                    i = i[:-3] + " " + i[-3:]
                    menu_list[ind] = i
            return "".join(menu_list)

        @staticmethod
        def inventory_armour_menu(armour_list: list):
            for i in armour_list:
                helmet, chest, leg, boots, ring1, ring2 = armour_list
            menu_line1 = " ------------------------------- \n"
            menu_line2 = "| Armour |\n"
            menu_line3 = "|-------------------------------|\n"
            menu_line4 = "| Helmet   | {} |\n".format(helmet.name)
            menu_line5 = "| Chest    | {} |\n".format(chest.name)
            menu_line6 = "| Leggings | {} |\n".format(leg.name)
            menu_line7 = "| Boots    | {} |\n".format(boots.name)
            menu_line8 = "| Ring 1   | {} |\n".format(ring1.name)
            menu_line9 = "| Ring 2   | {} |\n".format(ring2.name)
            menu_line10 = " ------------------------------- \n"
            menu_list = [menu_line1, menu_line2, menu_line3, menu_line4, menu_line5,
                         menu_line6, menu_line7, menu_line8, menu_line9, menu_line10]
            return Menus.InventoryMenus.inventory_menu_spacing(menu_list, [menu_line1, menu_line3, menu_line10])

        @staticmethod
        def inventory_weapon_menu(weapon_list: list):
            weapon1, weapon2, quiver = weapon_list
            menu_line1 = " ------------------------------- \n"
            menu_line2 = "| Weapons |\n"
            menu_line3 = "|-------------------------------|\n"
            menu_line4 = "| Weapon 1 | {} |\n".format(weapon1.name)
            menu_line5 = "| Weapon 2 | {} |\n".format(weapon2.name)
            menu_line6 = "| Quiver   | {} |\n".format(quiver)
            menu_line7 = " ------------------------------- \n"
            menu_list = [menu_line1, menu_line2, menu_line3, menu_line4,
                         menu_line5, menu_line6, menu_line7]
            return Menus.InventoryMenus.inventory_menu_spacing(menu_list, [menu_line1, menu_line3, menu_line7])

        @staticmethod
        def inventory_bag_menu(item_list: list):
            item1, item2, item3, item4, item5, item6, item7, item8, item9, item10 = item_list
            menu_line1 = " ------------------------------- \n"
            menu_line2 = "| Bag |\n"
            menu_line3 = "|-------------------------------|\n"
            menu_line4 = "| 1 - {} | 2 - {} |\n".format(item1, item2)
            menu_line5 = "| 3 - {} | 4 - {} |\n".format(item3, item4)
            menu_line6 = "| 5 - {} | 6 - {} |\n".format(item5, item6)
            menu_line7 = "| 7 - {} | 8 - {} |\n".format(item7, item8)
            menu_line8 = "| 9 - {} | 10 - {} |\n".format(item9, item10)
            menu_line9 = " ------------------------------- \n"
            menu_list = [menu_line1, menu_line2, menu_line3, menu_line4, menu_line5,
                         menu_line6, menu_line7, menu_line8, menu_line9]
            return Menus.InventoryMenus.inventory_menu_spacing(menu_list, [menu_line1, menu_line3, menu_line9])

    shop_menu_main = None
    shop_menu_buy = None
    shop_menu_sell = None
    load_save_menu = None


class Landscapes:
    main_village = "    888              \n" \
                   "    8888               ____[]\n" \
                   "    888               /    []\\\n" \
                   "   _| |              /     [] \\\n" \
                   " /  | |    ____     /          \\\n" \
                   "/______\\  /    \\     |   __   |\n" \
                   "|  _   |  |    |     |  |  |  | \n" \
                   "| | |  |  | [] |     |  |  |  |  \n"

    mountain = "       /\\         \n" \
               "      /AA\\        \n" \
               "     /-\\/-\\      \n" \
               "    /      \\      \n" \
               "   /        \\     \n" \
               "  /    __    \\    \n" \
               " /    {  }    \\   \n" \
               "/____/    \\____\\ \n"

    mountain_range = "           /\\              \n" \
                     "          /  \\             \n" \
                     "   /\\    /    \\  /\\      \n" \
                     "  /  \\  /      \\/  \\     \n" \
                     " / /\\ \\/       /    \\   \n" \
                     "/ /  \\ \\      /      \\  \n" \
                     " /    \\ \\    /        \\ \n" \
                     "/      \\ \\  /          \\\n"

    blocked_mountain = "       /\\         \n" \
                       "      /AA\\        \n" \
                       "     /-\\/-\\      \n" \
                       "    /      \\      \n" \
                       "   /        \\     \n" \
                       "  /    __    \\    \n" \
                       " /    {OO}    \\   \n" \
                       "/____/OOOO\\____\\ \n"

    tree1 = "        \n" \
            "        \n" \
            "        \n" \
            "  ****  \n" \
            " ****** \n" \
            "  ****  \n" \
            "   ||   \n" \
            "___||___\n"

    tree2 = "             \n" \
            "             \n" \
            "   /\\       \n" \
            "  //\\\\     \n" \
            " ///\\\\\\   \n" \
            "////\\\\\\\\ \n" \
            "   ||        \n" \
            "___||___     \n"

    tree2_close = "  /////////\\\\\\\\\\\\\\\\\\     \n" \
                  " //////////\\\\\\\\\\\\\\\\\\\\   \n" \
                  "///////////\\\\\\\\\\\\\\\\\\\\\\ \n" \
                  "        |\\||}|                    \n" \
                  "        ||||||                    \n" \
                  "        {|{|||                    \n" \
                  "        |||||{                    \n" \
                  "________||||]|____________________\n"


class Enemies:
    rat_passive = " (\\,/)                   \n" \
                  "  oo   '''//,        _    \n" \
                  ",/_;~,        \\,    / '  \n" \
                  "\"'   \\    (    \\    !  \n" \
                  "      ',|  \\    |__.'    \n" \
                  "      '~  '~----''\"      \n"

    rat_aggressive = "  ,     .             \n" \
                     "  (\\,;,/)            \n" \
                     "!  (o o)\\//,         \n" \
                     "    \\ /     \\,      \n" \
                     "    `+'(  (   \\    ) \n" \
                     "       //  \\   |_./  \n" \
                     "     '~' '~----'      \n"
print(Landscapes.mountain_range)