import json


class Tagging:
    from dataclasses import dataclass

    @dataclass
    class Hidden:
        def __init__(self, item_id: int, req_level: int, sellable: bool):
            self.item_id = item_id
            self.req_level = req_level
            self.sellable = sellable
            self.hidden = [item_id, req_level, sellable]
            self.hidden_template = {"Item_Id": self.item_id, "Req_Level": self.req_level,
                                    "Sellable": self.sellable}

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

            self.item_template = {"Name": self.name, "Item_type": self.item_type, "Dmg": self.dmg, "Crit": self.crit,
                                  "Special": self.special, "Price": self.price, "Hidden": self.hidden}


class Inventory:
    def __init__(self, character, new_player: bool):
        if new_player:
            self.newPlayer()
        else:
            self.character = character

    def __call__(self):
        return self.character

    def newPlayer(self):
        import queue
        from Items import ItemList
        player_save_bool = True
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
        weapons["Bag"].put((1, ItemList.rock))
        items = {"Armour": armour, "Weapons": weapons}
        self.character = {"Player_Save_Bool": player_save_bool, "Items": items, "Stats": stats, "Level": level}

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

    def loadPlayer():
        import queue
        from Items import ItemList
        with open("character.json", "r") as f:
            player_save = json.load(f)
            player_bag = player_save["Items"]["Weapons"]["Bag"]
            items = player_bag
            player_bag = queue.PriorityQueue(maxsize=10)
            for i in items:
                item = eval("ItemList.{}".format(i["Name"]))
                player_bag.put(i)
            Inventory(player_save, False)
            print("Success!")

    def savePlayer(self):
        bag_queue = self.character["Items"]["Weapons"]["Bag"]
        with open("character.json", "w") as f:
            bag = []
            for i in range(bag_queue.qsize()):
                item = bag_queue.get()
                item = item[1]
                hidden = item.hidden.hidden_template
                item = item.item_template
                item["Hidden"] = hidden
                bag.append(item)
            self.character["Items"]["Weapons"]["Bag"] = bag
            json.dump(self.character, f, indent=2)
            print("Success!")