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
                "Ring1": ItemList.wedding_ring,
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
        items = {"Armour": armour, "Weapons": weapons}
        self.character = {"Player_Save_Bool": player_save_bool, "Items": items, "Stats": stats, "Level": level}

    def getItem(self, item):
        bag_queue = self.character["Items"]["Weapons"]["Bag"]
        bag_item = bag_queue.get()
        while True:
            if bag_item != item:
                bag_queue.put(bag_item)
                bag_item = bag_queue.get()
            else:
                return bag_item

    class NoItem:
        def __init__(self):
            self.name = None

        def __call__(self):
            return self.name

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
        with open("character.json", "w") as f:
            bag = []
            for i in range(bag_queue.qsize()):
                item = bag_queue.get()
                hidden = item.hidden.hidden_template
                item = item.item_template
                item["Hidden"] = hidden
                bag.append(item)

            for key, value in self.character["Items"]["Armour"]["Rings"].items():
                if value is not None:
                    hidden = value.hidden.hidden_template
                    item = value.armour_template
                    item["Hidden"] = hidden
                    self.character["Items"]["Armour"]["Rings"][key] = item

            for key, value in self.character["Items"]["Armour"].items():
                if key != "Rings" and value is not None:
                    hidden = value.hidden.hidden_template
                    item = value.armour_template
                    item["Hidden"] = hidden
                    self.character["Items"]["Armour"][key] = item

            for key, value in self.character["Items"]["Weapons"]["Weapon_Slots"].items():
                if value is not None and key != "Bag":
                    hidden = value.hidden.hidden_template
                    item = value.item_template
                    item["Hidden"] = hidden
                    self.character["Items"]["Weapons"]["Weapon_Slots"][key] = item

            self.character["Items"]["Weapons"]["Bag"] = bag
            json.dump(self.character, f, indent=2)
            print("Success!")

    def inventorySetup(self):
        x = self.NoItem()
        armour_list = []
        for key, value in self.character["Items"]["Armour"].items():
            if key == "Rings":
                for ring_key, ring_value in self.character["Items"]["Armour"]["Rings"].items():
                    if ring_value is None:
                        ring_value = x
                        armour_list.append((ring_key, ring_value))
                    else:
                        armour_list.append((ring_key, ring_value))
            if value is None and key != "Rings":
                value = x
                armour_list.append((key, value))
            else:
                armour_list.append((key, value))

        weapon_list = []
        print(self.character["Items"]["Weapons"])
        for key, value in self.character["Items"]["Weapons"].items():
            if key == "Weapon_Slots":
                for weapon_key, weapon_value in self.character["Items"]["Weapons"]["Weapon_Slots"].items():
                    if weapon_value is None:
                        weapon_value = x
                        weapon_list.append((weapon_key, weapon_value))
                    else:
                        weapon_list.append((weapon_key, weapon_value))
            elif value is None and key != "Bag":
                value = x
                weapon_list.append((key, value))

            elif key != "Bag":
                weapon_list.append((key, value))

        bag_list = []
        bag_queue = self.character["Items"]["Weapons"]["Bag"]
        for i in range(bag_queue.qsize()):
            item = bag_queue.get()
            bag_list.append(item.name)
        while len(bag_list) < 10:
            bag_list.append(None)

        return armour_list, weapon_list, bag_list
