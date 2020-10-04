from InventorySystem import Tagging


class Item:
    rock = Tagging.Item("rock", "weapon", 1, 0, "", 0)
    basic_sword = Tagging.Item("Basic Sword", "weapon", 5, 0, "Nothing, what did you expect?", 1)


rock = Item().rock
print(rock.dmg)
