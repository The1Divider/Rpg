from InventorySystem import Tagging


class ItemList:
    rock = Tagging.Item("rock", "weapon", 1, 0, "", 0, Tagging.Hidden(0, None, False))
    basic_sword = Tagging.Item("Basic Sword", "weapon", 5, 0, "Nothing, what did you expect?", 1,
                               Tagging.Hidden(1, 2, True))
    item_dict = {"rock": rock, "basic_sword": basic_sword}
