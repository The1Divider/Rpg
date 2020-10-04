class Tagging:
    from dataclasses import dataclass

    @dataclass
    class Item:
        def __init__(self, name: str, item_type: str, dmg: int, crit: int, special: str, price: int):
            self.name = name
            self.item_type = item_type
            self.dmg = dmg
            self.crit = crit
            self.special = special
            self.price = price

def newPlayer():
    import queue
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
    weapons["Bag"].put((1, "Rock"))
    items = {"Armour": armour, "Weapons": weapons}
    character = {"Items": items, "Stats": stats, "Level": level}
    return character


class Inventory:
    def __init__(self, character_save, **character):
        import queue
        if not character_save:
            self.character = newPlayer()

    def getItem(self, item):
        wqueue = self.character["Items"]["Weapons"]["Bag"]
        bag_item = wqueue.get()

        while True:
            if bag_item[1] != item:
                bag_size = wqueue.qsize()
                bag_item = (bag_item[0] + bag_size + 1, bag_item[1])
                wqueue.put(bag_item)
                bag_item = wqueue.get()
            else:
                return bag_item

