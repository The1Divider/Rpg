from dataclasses import dataclass, field
from typing import NewType, Optional, List, Dict


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
    item_type: str
    item_weight: int
    dmg: int
    crit: int
    crit_chance: int
    special: str
    price: int
    hidden: Hidden

    item_template: Dict = field(init=False)

    def __post_init__(self):
        self.item_template = {'Name': self.name, 'Item_type': self.item_type, 'Item_weight': self.item_weight,
                              'Dmg': self.dmg, 'Crit': self.crit, 'Crit_Chance': self.crit_chance,
                              'Special': self.special, 'Price': self.price, 'Hidden': self.hidden}


@dataclass
class Armour:
    name: str = None
    item_type: str = None
    hp: int = None
    defence: int = None
    special: str = None
    price: int = None
    hidden: Hidden = None

    armour_template: Dict = field(init=False)

    def __post_init__(self):
        self.armour_template = {"Name": self.name, "Item_Type": self.item_type, "Hp": self.hp, "Defence": self.defence,
                                "Special": self.special, "Price": self.price, "Hidden": self.hidden}


HiddenType = NewType("HiddenType", Hidden)
ItemType = NewType("Item", Item)
ArmourType = NewType("Armour", Armour)


class ItemList:
    item_list = ["Rock", "Sticky Rock", "Basic Sword", "Copper Sword", "Iron Sword", "Steel Sword",
                 "Diamond-Cut Steel Sword", "Handcrafted Bow"]

    armour_list = ["Straw Sunhat", "Cotton Shirt", "Cotton Pants", "Straw Sandals", "Leather Helmet", "Leather Tunic",
                   "Leather Leggings", "Leather Boots", "Wedding Ring"]

    rock = Item(item_list[0], "weapon", 1, 1, 0, 0, "", 0, Hidden(1, None, False))
    sticky_rock = Item(item_list[1], "weapon", 1, 1, 0, 0, "Sticky", 0, Hidden(2, None, False))
    basic_sword_tag = "Nothing, what did you expect?"
    basic_sword = Item(item_list[2], "weapon", 1, 5, 0, 0, basic_sword_tag, 1, Hidden(3, None, True))
    copper_sword = Item(item_list[3], "weapon", 2, 5, 50, 5, "", 5, Hidden(4, 2, True))
    iron_sword = Item(item_list[4], "weapon", 2, 10, 50, 20, "", 10, Hidden(5, 5, True))
    steel_sword = Item(item_list[5], "weapon", 3, 15, 75, 20, "", 25, Hidden(6, 10, True))
    diamond_cut_steel_sword = Item(item_list[6], "weapon", 4, 25, 25, 10, "", 50, Hidden(7, 15, True))

    handcrafted_bow = Item(item_list[7], "weapon", 2, 5, 0, 0, "bow", 2, Hidden(8, 1, True))

    straw_sunhat = Armour(armour_list[0], "helmet", 1, 0, "", 1, Hidden(9, None, True))
    cotton_shirt = Armour(armour_list[1], "chestplate", 1, 0, "", 1, Hidden(10, None, True))
    cotton_pants = Armour(armour_list[2], "leggings", 1, 0, "", 1, Hidden(11, None, True))
    straw_sandals = Armour(armour_list[3], "boots", 1, 0, "", 1, Hidden(12, None, True))

    leather_helmet = Armour(armour_list[4], "helmet", 2, 10, "", 3, Hidden(13, 5, True))
    leather_tunic = Armour(armour_list[5], "chestplate", 5, 15, "", 5, Hidden(14, 5, True))
    leather_leggings = Armour(armour_list[6], "leggings", 2, 10, "", 3, Hidden(15, 5, True))
    leather_boots = Armour(armour_list[7], "boots", 2, 5, "", 2, Hidden(16, 5, True))

    wedding_ring_tag = "Your last memory of the real world"
    wedding_ring = Armour(armour_list[8], "ring", 0, 0, wedding_ring_tag, 0, Hidden(17, None, False))
