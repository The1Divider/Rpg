import json
from Items import *

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
            "Bag": queue.Queue(maxsize=10)
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
        weapons["Bag"].put(ItemList.rock)
        armour["Rings"]["Ring1"] = ItemList.wedding_ring
        items = {"Armour": armour, "Weapons": weapons}
        self.character = {"Player_Save_Bool": player_save_bool, "Items": items, "Stats": stats, "Level": level}

    def getItem(self, item):
        bag_queue = self.character["Items"]["Weapons"]["Bag"]
        bag_item = bag_queue.get()
        while True:
            if bag_item[1] != item:
                bag_queue.put(bag_item)
                bag_item = bag_queue.get()
            else:
                return bag_item

    def loadPlayer():
        import queue
        with open("character.json", "r") as f:
            player_save = json.load(f)
            player_bag = player_save["Items"]["Weapons"]["Bag"]
            items = player_bag
            player_bag = queue.Queue(maxsize=10)
            for i in items:
                item_name = i["Name"].lower().replace(" ", "_").replace("-", "_")
                item = eval("ItemList.{}".format(item_name))
                player_bag.put(item)
            Inventory(player_save, False)
            print("Success!")

    def savePlayer(self):
        bag_queue = self.character["Items"]["Weapons"]["Bag"]
        print(self.character["Items"]["Armour"]["Rings"]["Ring1"].name)
        with open("character.json", "w") as f:
            bag = []
            for i in range(bag_queue.qsize()):
                item = bag_queue.get()
                hidden = item.hidden.hidden_template
                item = item.item_template
                item["Hidden"] = hidden
                bag.append(item)
            print(self.character["Items"]["Armour"])
            for i in self.character["Items"]["Armour"]:
                print(i.item_type)
                hidden = i.hidden.hidden_template
                item = i.armour_template
                i["Hidden"] = hidden
                i = item
            self.character["Items"]["Weapons"]["Bag"] = bag
            json.dump(self.character, f, indent=2)
            print("Success!")
