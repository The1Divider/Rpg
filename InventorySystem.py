class Tagging:
    from dataclasses import dataclass

    @dataclass
    class Hidden:
        def __init__(self, item_id: int, req_level: int, sellable: bool):
            self.item_id = item_id
            self.req_level = req_level
            self.sellable = sellable
            self.hidden = [item_id, req_level, sellable]

    @dataclass
    class Item:
        def __init__(self, name: str, item_type: str, dmg: int, crit: int, special: str, price: int, hidden: list):
            self.name = name
            self.item_type = item_type
            self.dmg = dmg
            self.crit = crit
            self.special = special
            self.price = price
            self.hidden = hidden

        def save(self):
            self.hidden = {"Item_Id": self.hidden.item_id, "Req_Level": self.hidden.req_level, "Sellable": self.hidden.sellable}
            return {"Name": self.name, "Item_type": self.item_type, "Dmg": self.dmg, "Crit": self.crit,
                    "Special": self.special, "Price": self.price, "Hidden": self.hidden}

        def load(self):
            pass


def newPlayer():
    import queue
    import Items
    armour = {
        "Helmet": None,
        "Chestplate": None,
        "Legs": None,
        "Boots": None,
        "Rings": {
            "Ring1": None,
            "Ring2": None
        }
    }
    weapons = {
        "Weapon_Slots": {
            "Weapon1": None,
            "Weapon2": None,
        },
        "Quiver": None,
        "Sheath": None,
        "Bag": queue.PriorityQueue(maxsize=10)
    }
    stats = {
        "HP": 10,
        "Dmg": 1,
        "Def": 0,
        "Crit": 0,
        "Block": 0
    }
    level = {
        "Difficulty": None,
        "Enemy_Level": 1,
        "Player_Level": 1,
    }
    weapons["Bag"].put((1, Items.Item.rock))
    items = {"Armour": armour, "Weapons": weapons}
    character = {"Items": items, "Stats": stats, "Level": level}
    return character


class Inventory:
    def __init__(self, character_save, **character):
        import queue
        if not character_save:
            self.character = newPlayer()

    def getItem(self, item):
        bag_queue = self.character["Items"]["Weapons"]["Bag"]
        bag_item = bag_queue.get()

        while True:
            if bag_item[1] != item:
                bag_size = bag_queue.qsize()
                bag_item = (bag_item[0] + bag_size + 1, bag_item[1])
                bag_queue.put(bag_item)
                bag_item = bag_queue.get()
            else:
                return bag_item


