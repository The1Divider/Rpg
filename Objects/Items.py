from dataclasses import dataclass, field
from typing import NewType, Optional, Dict, Union


@dataclass
class UnknownItem:
    name = None
    item_weight: int = 0
    dmg: int  = 0
    crit: int = 0
    crit_chance: int = 0
    special = None
    price: int = 0
    hidden = None


@dataclass
class UnknownArmour:
    name = None
    hp = 0
    defence = 0
    special = 0
    price = 0
    hidden = None


@dataclass
class Hidden:
    item_id: int
    req_level: Optional[int]
    sellable: bool
    hidden_template: Dict = field(init=False)

    def __post_init__(self):
        self.hidden_template = {"Item_Id": self.item_id, "Req_Level": self.req_level, "Sellable": self.sellable}


@dataclass
class Item:
    name: str
    item_weight: int
    dmg: int
    crit: int
    crit_chance: int
    special: str
    price: int
    hidden: Hidden

    item_template: Dict = field(init=False)

    def __post_init__(self):
        self.item_template = {'Name': self.name, 'Item_weight': self.item_weight,
                              'Dmg': self.dmg, 'Crit': self.crit, 'Crit_Chance': self.crit_chance,
                              'Special': self.special, 'Price': self.price, 'Hidden': self.hidden}


@dataclass
class Armour:
    name: str
    hp: int
    defence: int
    special: str
    price: int
    hidden: Hidden

    armour_template: Dict = field(init=False)

    def __post_init__(self):
        self.armour_template = {"Name": self.name, "Hp": self.hp, "Defence": self.defence,
                                "Special": self.special, "Price": self.price, "Hidden": self.hidden}


UnknownItemType = UnknownItem
UnknownArmourType = UnknownArmour
HiddenType = Hidden
ItemType = Item
ArmourType = Armour


class ItemList:
    item_list = ["Rock", "Sticky Rock", "Basic Sword", "Copper Sword", "Iron Sword", "Steel Sword",
                 "Diamond-Cut Steel Sword", "Handcrafted Bow"]

    armour_list = ["Straw Sunhat", "Cotton Shirt", "Cotton Pants", "Straw Sandals", "Leather Helmet", "Leather Tunic",
                   "Leather Leggings", "Leather Boots", "Wedding Ring"]

    rock = Item(item_list[0], 1, 1, 0, 0, "", 0, Hidden(1, None, False))
    sticky_rock = Item(item_list[1], 1, 1, 0, 0, "Sticky", 0, Hidden(2, None, False))
    basic_sword_tag = "Nothing, what did you expect?"
    basic_sword = Item(item_list[2], 1, 5, 0, 0, basic_sword_tag, 1, Hidden(3, None, True))
    copper_sword = Item(item_list[3], 2, 5, 50, 5, "", 5, Hidden(4, 2, True))
    iron_sword = Item(item_list[4], 2, 10, 50, 20, "", 10, Hidden(5, 5, True))
    steel_sword = Item(item_list[5], 3, 15, 75, 20, "", 25, Hidden(6, 10, True))
    diamond_cut_steel_sword = Item(item_list[6], 4, 25, 25, 10, "", 50, Hidden(7, 15, True))

    handcrafted_bow = Item(item_list[7], 2, 5, 0, 0, "", 2, Hidden(8, 1, True))

    straw_sunhat = Armour(armour_list[0], 1, 0, "", 1, Hidden(9, None, True))
    cotton_shirt = Armour(armour_list[1], 1, 0, "", 1, Hidden(10, None, True))
    cotton_pants = Armour(armour_list[2], 1, 0, "", 1, Hidden(11, None, True))
    straw_sandals = Armour(armour_list[3], 1, 0, "", 1, Hidden(12, None, True))

    leather_helmet = Armour(armour_list[4], 2, 10, "", 3, Hidden(13, 5, True))
    leather_tunic = Armour(armour_list[5], 5, 15, "", 5, Hidden(14, 5, True))
    leather_leggings = Armour(armour_list[6], 2, 10, "", 3, Hidden(15, 5, True))
    leather_boots = Armour(armour_list[7], 2, 5, "", 2, Hidden(16, 5, True))

    wedding_ring_tag = "Your last memory of the real world"
    wedding_ring = Armour(armour_list[8], 0, 0, wedding_ring_tag, 0, Hidden(17, None, False))
