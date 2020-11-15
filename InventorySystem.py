import json
import queue
from contextlib import suppress
from dataclasses import dataclass
from typing import List, Optional, Tuple

from Items import ItemList, Tagging

ItemType = Tagging.ItemType
ArmourType = Tagging.ArmourType


@dataclass
class Armour:
    """Set player armour attributes"""
    def __init__(self) -> None:
        self.helmet = None
        self.chestplate = None
        self.leggings = None
        self.boots = None
        self.ring1 = None
        self.ring2 = None


@dataclass
class Weapons:
    """Set player weapon attributes"""
    def __init__(self) -> None:
        self.weapon1 = None
        self.weapon2 = None
        self.quiver = 0


@dataclass
class Stats:
    """Set player stats attributes"""
    def __init__(self) -> None:
        self.crit_chance = None
        self.hp = 10
        self.dmg = 1
        self.defence = 0
        self.crit = 0
        self.block = 0


@dataclass
class Levels:
    """Set player level attributes"""
    def __init__(self) -> None:
        self.difficulty = None
        self.player_level = 1
        self.player_exp = 0


class Inventory:
    def __init__(self, dev_mode: bool = False) -> None:
        self.exp_bar = None
        self.required_exp_percent = 0
        self.required_exp = 0
        self.dev_mode = dev_mode
        self.queue_max_size = 10
        self.Armour = Armour()
        self.Weapons = Weapons()
        self.Stats = Stats()
        self.Levels = Levels()
        self.bag = queue.Queue(maxsize=self.queue_max_size)
        self.armour_slots = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
        self.weapon_slots = ["weapon1", "weapon2", "quiver"]
        self.stat_slots = ["hp", "dmg", "defence", "crit", "block"]
        self.armour_list_temp = []
        self.weapon_list_temp = []
        self.bag_list_temp = []
        self.stat_list_temp = []

    def new_player(self) -> None:
        """give new player preset items"""
        self.Armour.ring1 = ItemList.wedding_ring
        self.bag.put(ItemList.rock)
        self.Armour.helmet = ItemList.straw_sunhat

    def equip_weapon(self, weapon: str) -> None:
        to_replace = None
        item = self.get_item(weapon, select=True)
        weight_item, weight_slot_1, weight_slot_2 = None, None, None

        with suppress(AttributeError):
            weight_item = item.item_weight
            weight_slot_1 = self.Weapons.weapon1.item_weight
            weight_slot_2 = self.Weapons.weapon2.item_weight

        if item is not None:

            if weight_item == 1 and (weight_slot_1 is None or weight_slot_2 is None):
                slot = "weapon1" if self.Weapons.weapon1 is None else "weapon2"
                setattr(self.Weapons, slot, item)
                return None

            else:
                while (slot := input(f"Which slot do you want to replace with {item.name}").lower().replace(" ", ""))\
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
                return None

            if weight_item == 2 and (self.Weapons.weapon1 is None and self.Weapons.weapon2 is None):
                setattr(self.Weapons, "weapon1", item)

            else:
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
            print("Invalid weapon")
            return None

    def get_item(self, item: str, select: bool = False) -> Optional[ItemType]:
        """iterate through items in bag to get specified item"""
        bag_item_temp = None
        bag_queue = self.bag
        size = bag_queue.qsize()
        bag_item = bag_queue.get()
        print(bag_item.name.lower(), item, size)

        while bag_item.name.lower() != item and size > 0:
            bag_queue.put(bag_item)
            bag_item = bag_queue.get()
            size -= 1

        if bag_item is not None and not select:
            bag_item_temp = bag_item
            bag_queue.put(bag_item)
            bag_item = bag_item_temp

        return bag_item

    @property
    def armour_list(self) -> List[Optional[ArmourType]]:
        return [getattr(self.Armour, attribute) for attribute in self.armour_slots]

    @property
    def weapon_list(self) -> List[Optional[ItemType]]:
        return [getattr(self.Weapons, attribute) for attribute in self.weapon_slots]

    @property
    def stat_list(self) -> List[int]:
        return [getattr(self.Stats, attribute) for attribute in self.stat_slots]

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

    def save_player(self):
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
                        item = value.weapon_template

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

    def inventory_setup(self):
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

    def stats_setup(self) -> None:

        def exp() -> Tuple[float, int]:
            level_with_decimal = (((100 * (2 * self.Levels.player_exp + 25)) ** (1 / 2)) + 50) / 100
            next_level = int(level_with_decimal) + 1
            next_level_exp = (next_level ** 2 + next_level) / 2 * 100 - (next_level * 100)

            required_exp = next_level_exp - self.Levels.player_exp
            required_exp_percent = self.required_exp / next_level_exp * 100
            return required_exp, required_exp_percent

        hp, dmg, defence, crit, block = (self.Stats.hp, self.Stats.dmg, self.Stats.defence,
                                         self.Stats.crit, self.Stats.block)
        armour_hp, armour_defence = 0, 0
        weapon_dmg, weapon_crit = 0, 0
        stats = self.stat_list

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

            except AttributeError:
                pass

        exp, exp_percent = exp()

        self.stat_list_temp = [hp, armour_hp, dmg, weapon_dmg, defence, armour_defence, crit, weapon_crit, block,
                               self.Levels.player_level, exp, exp_percent]
