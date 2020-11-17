import json
import queue
from contextlib import suppress
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union, Any

from Objects.Items import ItemList, ItemType, ArmourType
from Objects.Sprites import MenuSprites, MenuType


@dataclass
class Armour:
    """Set player armour attributes"""
    helmet: Optional[ArmourType] = None
    chestplate: Optional[ArmourType] = None
    leggings: Optional[ArmourType] = None
    boots: Optional[ArmourType] = None
    ring1: Optional[ArmourType] = None
    ring2: Optional[ArmourType] = None


@dataclass
class Weapons:
    """Set player weapon attributes"""
    weapon1: Optional[ItemType] = None
    weapon2: Optional[ItemType] = None
    quiver: int = 0


@dataclass
class Stats:
    """Set player stats attributes"""
    current_hp: int = field(init=False)
    hp: int = 10
    dmg: int = 1
    defence: int = 0
    crit: int = 0
    crit_chance: int = 0
    block: int = 0

    def __post_init__(self):
        self.current_hp = self.hp


@dataclass
class Levels:
    """Set player level attributes"""
    difficulty: Optional[int] = None
    player_level: int = 1
    player_exp: int = 0


class Inventory:
    def __init__(self, dev_mode: bool = False) -> None:
        self.dev_mode: bool = dev_mode

        self.exp_bar: Optional[int] = None
        self.required_exp_percent: int = 0
        self.required_exp: int = 0

        self.queue_max_size: int = 10
        self.bag: queue.Queue = queue.Queue(maxsize=self.queue_max_size)

        self.Armour: Armour = Armour()
        self.Weapons: Weapons = Weapons()
        self.Stats: Stats = Stats()
        self.Levels: Levels = Levels()

        self.armour_slots: list = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
        self.weapon_slots: list = ["weapon1", "weapon2", "quiver"]
        self.stat_slots: list = ["hp", "dmg", "defence", "crit", "crit_chance", "block"]

        self.armour_list_temp: list = []
        self.weapon_list_temp: list = []
        self.bag_list_temp: list = []
        self.stat_list_temp: list = []

    @property
    def armour_list(self) -> List[Optional[ArmourType]]:
        return [getattr(self.Armour, attribute) for attribute in self.armour_slots]

    @property
    def weapon_list(self) -> List[Optional[ItemType]]:
        return [getattr(self.Weapons, attribute) for attribute in self.weapon_slots]

    @property
    def stat_list(self) -> List[int]:
        return [getattr(self.Stats, attribute) for attribute in self.stat_slots]

    def new_player(self) -> None:
        """give new player preset items"""
        self.Armour.ring1 = ItemList.wedding_ring
        self.bag.put(ItemList.rock)
        self.Armour.helmet = ItemList.straw_sunhat

    def save_player(self) -> None:
        """Set armour/weapons/stats/levels/bag to dicts and dump to JSON"""
        arm, wep, stat, lev = self.Armour, self.Weapons, self.Stats, self.Levels
        armour_dict = {"Helmet": arm.helmet, "Chestplate": arm.chestplate, "Leggings": arm.leggings,
                       "Boots": arm.boots, "Ring1": arm.ring1, "Ring2": arm.ring2}
        weapon_dict = {"Weapon1": wep.weapon1, "Weapon2": wep.weapon2, "Quiver": wep.quiver}
        stat_dict = {"Hp": stat.hp, "Dmg": stat.dmg, "Defence": stat.defence, "Crit": stat.crit, "Block": stat.block}
        level_dict = {"Difficulty": lev.difficulty, "Player Level": lev.player_level}
        bag = []
        bag_queue = self.bag

        for _ in range(bag_queue.qsize()):
            item = bag_queue.get()
            hidden = item.hidden.hidden_template
            item = item.item_template
            item["Hidden"] = hidden
            bag.append(item)

        dicts = [("weapon", weapon_dict), ("armour", armour_dict)]

        for subdict in dicts:

            for key, value in subdict[1].items():

                if value is not None and key != "Quiver":
                    hidden = value.hidden.hidden_template

                    if subdict[0] == "weapon":
                        item = value.item_template

                    else:
                        item = value.armour_template

                    item["Hidden"] = hidden
                    subdict[1][key] = item

        with open("character.json", "w") as f:
            player = {"Armour": armour_dict, "Weapons": weapon_dict, "Bag": bag,
                      "Stats": stat_dict, "Levels": level_dict}
            json.dump(player, f, indent=2)
            f.close()
            print("Success!")

        return None

    def load_player(self) -> None:
        with open("character.json", "r") as f:
            player = json.load(f)
            f.close()

        player_dict_keys = ["Weapons", "Armour"]
        player_dicts = [player[key] for key in player_dict_keys]

        for subdict in player_dicts:

            dict_keys = player_dict_keys[player_dicts.index(subdict)]

            for key, value in subdict.items():

                if value is not None and key != "Quiver":
                    key = key.lower()
                    value = value["Name"].lower().replace(" ", "_")
                    exec(f"self.{dict_keys}.{key} = ItemList.{value}")

        self.Weapons.quiver = player["Weapons"]["Quiver"]

        stats = player["Stats"]

        for key, value in stats.items():
            setattr(self.Stats, str(value), getattr(self.Stats, key.lower()))

        items = player["Bag"]
        player_bag = queue.Queue(maxsize=10)

        for item in items:
            item_name = item["Name"].lower().replace(" ", "_")
            item = getattr(ItemList, item_name)
            player_bag.put(item)

        self.bag = player_bag

        print("Success!")

        return None

    def equip_weapon(self, weapon: Optional[str], index: Optional[int] = None) -> None:
        to_replace = None
        item = self.get_item(weapon, index, select=True)
        weight_item, weight_slot_1, weight_slot_2 = None, None, None

        if item == -1:
            print("Invalid choice")
            return None

        with suppress(AttributeError):
            weight_item = item.item_weight
            weight_slot_1 = self.Weapons.weapon1.item_weight
            weight_slot_2 = self.Weapons.weapon2.item_weight

        if item is not None:

            if weight_item == 1 and (weight_slot_1 is None or weight_slot_2 is None):
                slot = "weapon1" if self.Weapons.weapon1 is None else "weapon2"
                setattr(self.Weapons, slot, item)
                return None

            elif weight_item == 1 and (weight_slot_1 is not None and weight_slot_2 is not None):
                while (slot := input(f"Which slot do you want to replace with {item.name}").lower().replace(" ", "")) \
                        not in ("slot1", "slot2", "cancel"):
                    print("Invalid slot (slot 1, slot 2, cancel")

                if slot == "slot1":
                    to_replace = getattr(self.Weapons, "weapon1")
                    setattr(self.Weapons, "weapon1", item)

                elif slot == "slot2":
                    to_replace = getattr(self.Weapons, "weapon2")
                    setattr(self.Weapons, "weapon2", item)

                elif slot == "cancel":
                    to_replace = item

                self.bag.put(to_replace)

            elif weight_item == 2 and (weight_slot_1 is None and weight_slot_2 is None):
                setattr(self.Weapons, "weapon1", item)

            elif weight_item == 2 and (weight_slot_1 is not None and weight_slot_2 is not None):
                while (ans := input(f"Do you want to replace your current weapons with {item.name}?\n").lower()) not \
                        in ("yes", 'y', "no", 'n'):
                    print("Invalid choice (y/n)")

                if ans in ("yes", 'y'):
                    weapon_1, weapon_2 = [getattr(self.Weapons, attribute) for attribute in ("weapon1", "weapon2")]
                    print(weapon_1, weapon_2)
                    self.bag.put(weapon_1)
                    self.bag.put(weapon_2)
                    setattr(self.Weapons, "weapon1", item)

                elif ans in ("no", 'n'):
                    self.bag.put(item)

            return None

        else:
            print("Invalid weapon, your bag is empty")
            return None

    def get_item(self, item: Optional[str], index: Optional[int] = None, select: bool = False) \
            -> Optional[Union[ItemType, int]]:
        """iterate through items in bag to get specified item"""
        bag_item_temp = None
        bag_queue = self.bag
        size = bag_queue.qsize()

        if size != 0 and (index is not None and index <= size):
            bag_item = bag_queue.get()

        else:
            return None

        while bag_item.name.lower() != item and size > 0 and index >= 1:
            bag_queue.put(bag_item)
            bag_item = bag_queue.get()
            size -= 1
            index -= 1

        if bag_item.name.lower() != item and item is not None:
            bag_queue.put(bag_item)
            return -1

        if bag_item is not None and not select:
            bag_item_temp = bag_item
            bag_queue.put(bag_item)
            bag_item = bag_item_temp

        return bag_item

    def inventory_setup(self) -> None:
        """Create instances of armour and items to send to inventory display w/o mutating the inventory.
           Also copies items in bag to prevent having to return them"""

        class NoItem:
            """Placeholder for attribute of a nonexistent item"""

            def __init__(self):
                self.name = None

        x = NoItem()

        for item in self.armour_list:
            if item is None:
                item = x
            self.armour_list_temp.append(item)

        for item in self.weapon_list:
            if item is None:
                item = x
            self.weapon_list_temp.append(item)

        bag_queue = self.bag

        for _ in range(bag_queue.qsize()):
            temp = bag_queue.get()
            item = temp
            bag_queue.put(temp)
            self.bag_list_temp.append(item.name)

        while len(self.bag_list_temp) < self.queue_max_size:
            self.bag_list_temp.append(None)

        return None

    def stats_setup(self, in_loop: bool) -> Tuple[List[Union[int, Any]], Optional[int]]:
        """
        :return: [hp, armour_hp, dmg, weapon_dmg, defence, armour_defence, crit, weapon_crit, crit_chance,
                  weapon_crit_chance, block, self.Levels.player_level, exp, exp_percent]
        """
        def exp() -> Tuple[float, int, int]:
            level_with_decimal = (((100 * (2 * self.Levels.player_exp + 25)) ** (1 / 2)) + 50) / 100
            level_int = int(level_with_decimal)
            next_level = level_int + 1
            next_level_exp = (next_level ** 2 + next_level) / 2 * 100 - (next_level * 100)

            required_exp = next_level_exp - self.Levels.player_exp
            required_exp_percent = required_exp / next_level_exp * 100

            return required_exp, required_exp_percent, level_int

        hp, dmg, defence, crit, crit_chance, block = self.stat_list
        armour_hp, armour_defence = 0, 0
        weapon_dmg, weapon_crit, weapon_crit_chance = 0, 0, 0

        for armour in self.armour_list:

            try:
                armour_hp += armour.hp
                armour_defence += armour.defence

            except AttributeError:
                pass

        for weapon in self.weapon_list:

            try:
                weapon_dmg += weapon.dmg
                weapon_crit += weapon.crit
                weapon_crit_chance += weapon.crit_chance

            except AttributeError:
                pass

        exp, exp_percent, level = exp()
        setattr(self.Levels, "player_level", level)
        self.stat_list_temp = [hp, armour_hp, dmg, weapon_dmg, defence, armour_defence, crit, weapon_crit, crit_chance,
                               weapon_crit_chance, block, self.Levels.player_level, exp, exp_percent]

        if in_loop:
            current_hp = self.Stats.current_hp

        else:
            current_hp = None

        return self.stat_list_temp, current_hp

    def inventory_display(self) -> None:
        """Displays with setup"""
        self.inventory_setup()
        a, w, b = self.armour_list_temp, self.weapon_list_temp, self.bag_list_temp
        armours = MenuSprites.InventoryMenus.inventory_armour_menu(a)
        weapons = MenuSprites.InventoryMenus.inventory_weapon_menu(w)
        bag = MenuSprites.InventoryMenus.inventory_bag_menu(b)
        self.armour_list_temp, self.weapon_list_temp, self.bag_list_temp = [], [], []

        def armour_menu() -> Optional[MenuType]:
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
                    print(MenuSprites.InventoryMenus.armour_selection(getattr(self.Armour, armour_selection)))

                else:
                    armour_selection = armour_selection.title()
                    armour_list = [getattr(self.Armour, attribute) for attribute in armour_selection_list]

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
                self.bag_list_temp = []
                return None

        def weapon_menu() -> Optional[MenuType]:
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
                    print(MenuSprites.InventoryMenus.weapon_selection(getattr(self.Weapons, weapon_selection)))
                    return weapon_menu()

                else:
                    weapon_selection = weapon_selection.title()
                    weapon_list = [getattr(self.Weapons, attribute) for attribute in ("weapon1", "weapon2")]

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
                return None

        def bag_menu() -> Optional[MenuType]:
            input_message = "1) Select Item, 2) Equip Weapon, 3) Previous Page, 4) Exit\n"
            print(bag)

            while (selection := input(input_message)) not in ("1", "2", "3", "4"):
                print("Invalid Selection")

            if selection == "1":

                weapon_selection = input("Selection: ").lower().replace(" ", "_")

                if weapon_selection in [str(number) for number in range(1, 11)]:
                    index = int(weapon_selection)
                    weapon_selection = None

                else:
                    index = None

                item = self.get_item(weapon_selection, index)

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

                if weapon in [str(number) for number in range(1, 11)]:
                    index = int(weapon)
                    weapon = None

                else:
                    index = None

                self.equip_weapon(weapon, index)
                return self.inventory_display()

            elif selection == "3":
                return weapon_menu()

            elif selection == "4":
                self.bag_list_temp = []
                return None

        armour_menu()

    def stats_display(self, in_loop: bool):
        """Setup and display player stats + armour/weapon stats"""
        stats_list, current_hp = self.stats_setup(in_loop)
        stat_display = MenuSprites.InventoryMenus.stats_menu(stats_list, current_hp)
        print(stat_display)
        return None
