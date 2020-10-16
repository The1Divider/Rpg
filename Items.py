class Tagging:
    from dataclasses import dataclass

    @dataclass
    class Hidden:
        def __init__(self, item_id: int, req_level, sellable: bool):
            self.item_id = item_id
            self.req_level = req_level
            self.sellable = sellable
            self.hidden = [item_id, req_level, sellable]
            self.hidden_template = {"Item_Id": self.item_id, "Req_Level": self.req_level,
                                    "Sellable": self.sellable}

    @dataclass
    class Item:
        def __init__(self, name: str, item_type: str, item_weight: int, dmg: int,
                     crit: int, crit_chance: int, special: str, price: int, hidden):
            self.name = name
            self.item_type = item_type
            self.item_weight = item_weight
            self.dmg = dmg
            self.crit = crit
            self.crit_chance = crit_chance
            self.special = special
            self.price = price
            self.hidden = hidden

            self.item_template = {"Name": self.name, "Item_type": self.item_type, "Dmg": self.dmg, "Crit": self.crit,
                                  "Special": self.special, "Price": self.price, "Hidden": self.hidden}

    @dataclass
    class Armour:
        def __init__(self, name: str, item_type: str, hp: int, defence: int, special: str, price: int, hidden):
            self.name = name
            self.item_type = item_type
            self.hp = hp
            self.defence = defence
            self.special = special
            self.price = price
            self.hidden = hidden

            self.armour_template = {"Name": self.name, "Item_Type": self.item_type, "Hp": self.hp,
                                    "Defence": self.defence, "Special": self.special, "Price": self.price,
                                    "Hidden": self.hidden}


class ItemList:
    item_list = ["Rock", "Sticky Rock", "Basic Sword", "Copper Sword", "Iron Sword", "Steel Sword",
                 "Diamond-Cut Steel Sword", "Handcrafted Bow"]

    armour_list = ["Straw Sunhat", "Cotton Shirt", "Cotton_pants", "Straw Sandals", "Leather Helmet", "Leather Tunic",
                   "Leather Leggings", "Leather Boots", "Wedding Ring"]

    rock = Tagging.Item(item_list[0], "weapon", 1, 1, 0, 0, "", 0, Tagging.Hidden(1, None, False))
    sticky_rock = Tagging.Item(item_list[1], "weapon", 1, 1, 0, 0, "Sticky", 0, Tagging.Hidden(2, None, False))
    basic_sword_tag = "Nothing, what did you expect?"
    basic_sword = Tagging.Item(item_list[2], "weapon", 1, 5, 0, 0, basic_sword_tag, 1, Tagging.Hidden(3, None, True))
    copper_sword = Tagging.Item(item_list[3], "weapon", 2, 5, 50, 5, "", 5, Tagging.Hidden(4, 2, True))
    iron_sword = Tagging.Item(item_list[4], "weapon", 2, 10, 50, 20, "", 10, Tagging.Hidden(5, 5, True))
    steel_sword = Tagging.Item(item_list[5], "weapon", 3, 15, 75, 20, "", 25, Tagging.Hidden(6, 10, True))
    diamond_cut_steel_sword = Tagging.Item(item_list[6], "weapon", 4, 25, 25, 10, "", 50, Tagging.Hidden(7, 15, True))

    handcrafted_bow = Tagging.Item(item_list[7], "weapon", 2, 5, 0, 0, "bow", 2, Tagging.Hidden(8, 1, True))

    straw_sunhat = Tagging.Armour(armour_list[0], "helmet", 1, 0, "", 1, Tagging.Hidden(9, None, True))
    cotton_shirt = Tagging.Armour(armour_list[1], "chestplate", 1, 0, "", 1, Tagging.Hidden(10, None, True))
    cotton_pants = Tagging.Armour(armour_list[2], "pants", 1, 0, "", 1, Tagging.Hidden(11, None, True))
    straw_sandals = Tagging.Armour(armour_list[3], "shoes", 1, 0, "", 1, Tagging.Hidden(12, None, True))

    leather_helmet = Tagging.Armour(armour_list[4], "helmet", 2, 10, "", 3, Tagging.Hidden(13, 5, True))
    leather_tunic = Tagging.Armour(armour_list[5], "chestplate", 5, 15, "", 5, Tagging.Hidden(14, 5, True))
    leather_leggings = Tagging.Armour(armour_list[6], "pants", 2, 10, "", 3, Tagging.Hidden(15, 5, True))
    leather_boots = Tagging.Armour(armour_list[7], "shoes", 2, 5, "", 2, Tagging.Hidden(16, 5, True))

    wedding_ring_tag = "Your last memory of the real world"
    wedding_ring = Tagging.Armour(armour_list[8], "ring", 0, 0, wedding_ring_tag, 0, Tagging.Hidden(17, None, False))
