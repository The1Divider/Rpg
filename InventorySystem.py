import json
from Items import ItemList
import queue
from dataclasses import dataclass


@dataclass()
class Armour:
    def __init__(self):
        self.helmet = None
        self.chestplate = None
        self.leggings = None
        self.boots = None
        self.ring1 = None
        self.ring2 = None


@dataclass()
class Weapons:
    def __init__(self):
        self.weapon1 = None
        self.weapon2 = None
        self.quiver = 0


@dataclass()
class Stats:
    def __init__(self):
        self.hp = 10
        self.dmg = 1
        self.defence = 0
        self.crit = 0
        self.block = 0


@dataclass()
class Levels:
    def __init__(self):
        self.difficulty = None
        self.enemy_level = 1
        self.player_level = 1


class Inventory:
    def __init__(self):
        self.queue_max_size = 10
        self.Armour = Armour()
        self.Weapons = Weapons()
        self.Stats = Stats()
        self.Levels = Levels()
        self.bag = queue.Queue(maxsize=self.queue_max_size)
        self.armour_slots = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
        self.weapon_slots = ["weapon1", "weapon2", "quiver"]

    def new_player(self):
        self.Armour.ring1 = ItemList.wedding_ring
        self.bag.put(ItemList.rock)

    def get_item(self, item):
        bag_queue = self.bag
        bag_item = bag_queue.get()
        while bag_item.name != item:
            bag_queue.put(bag_item)
            bag_item = bag_queue.get()
        return bag_item

    @property
    def armour_list(self):
        return [getattr(self.Armour, attribute) for attribute in self.armour_slots]

    @property
    def weapon_list(self):
        return [getattr(self.Weapons, attribute) for attribute in self.weapon_slots]

    # this still needs to be fixed
    def load_player(self):
        with open("character.json", "r") as f:
            player = json.load(f)
            f.close()
        player_bag = player["Items"]["Bag"]
        items = player_bag
        player_bag = queue.Queue(maxsize=10)
        for item in items:
            item_name = item["Name"].lower().replace(" ", "_").replace("-", "_")
            item = eval("ItemList.{}".format(item_name))
            player_bag.put(item)
        Inventory()
        print("Success!")

    def save_player(self):
        arm, wep, stat, lev = self.Armour, self.Weapons, self.Stats, self.Levels
        armour_dict = {"Helmet": arm.helmet, "Chestplate": arm.chestplate, "Leggings": arm.leggings,
                       "Boots": arm.boots, "Ring1": arm.ring1, "Ring2": arm.ring2}
        weapon_dict = {"Weapon1": wep.weapon1, "Weapon2": wep.weapon2, "Quiver": wep.quiver}
        stat_dict = {"Hp": stat.hp, "Dmg": stat.dmg, "Def": stat.defence, "Crit": stat.crit, "Block": stat.block}
        level_dict = {"Difficulty": lev.difficulty, "Enemy Level": lev.enemy_level, "Player Level": lev.player_level}
        bag = []
        bag_queue = self.bag

        for _ in range(bag_queue.qsize()):
            item = bag_queue.get()
            hidden = item.hidden.hidden_template
            item = item.item_template
            item["Hidden"] = hidden
            bag.append(item)

        # converting item to dict object
        for key, armour in armour_dict.items():
            if armour is not None:
                hidden = armour.hidden.hidden_template
                item = armour.armour_template
                item["Hidden"] = hidden
                armour_dict[key] = item

        for key, weapon in weapon_dict.items():
            if weapon is not None and key != "Quiver":
                hidden = weapon.hidden.hidden_template
                item = weapon.item_template
                item["Hidden"] = hidden
                weapon_dict[key] = item

        with open("character.json", "w") as f:
            player = {"Armour": armour_dict, "Weapons": weapon_dict, "Bag": bag,
                      "Stats": stat_dict, "Levels": level_dict}
            json.dump(player, f, indent=2)
            f.close()
            print("Success!")

    class NoItem:
        def __init__(self):
            self.name = None

        def __call__(self):
            return self.name

    def inventory_setup(self):
        x = self.NoItem()  # Placeholder for a .name attribute if no item


        self.armour_list_temp = []
        for item in self.armour_list:
            if item is None:
                item = x
            self.armour_list_temp.append(item)

        self.weapon_list_temp = []
        for item in self.weapon_list:
            if item is None:
                item = x
            self.weapon_list_temp.append(item)

        # Lists items in bag without mutating the queue
        self.bag_list_temp = []
        bag_queue = self.bag
        for _ in range(bag_queue.qsize()):
            temp = bag_queue.get()
            item = temp
            bag_queue.put(temp)
            self.bag_list_temp.append(item.name)
        while len(self.bag_list_temp) < self.queue_max_size:
            self.bag_list_temp.append(None)

