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


class Inventory:

    def __init__(self, character_save, **character):
        import queue
        if not character_save:
            self.armour = {
                "Helmet": None,
                "Chestplate": None,
                "Legs": None,
                "Boots": None,
                "Rings": {
                    "Ring1": None,
                    "Ring2": None
                    }
               }
            self.weapons = {
                "Weapon1": None,
                "Weapon2": None,
                "Quiver": None,
                "Sheath": None,
                "Bag": queue.PriorityQueue(maxsize=10)
            }
            self.stats = {
                "HP": 10,
                "Dmg": 1,
                "Def": 0,
                "Crit": 0,
                "Block": 0
            }
            self.weapons["Bag"].put((2, "rock"))
            self.weapons["Bag"].put((1, "chicken"))

    def getItem(self, item):
        wqueue = self.weapons["Bag"]
        weapon = wqueue.get()

        while True:
            if weapon[1] != item:
                bag_size = wqueue.qsize()
                weapon = (weapon[0] + bag_size + 1, weapon[1])
                wqueue.put(weapon)
                weapon = wqueue.get()
            else:
                return weapon

Inventory(False)
print(Inventory(False).getItem('rock'))
