import json
import queue
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple, Literal, overload, Union

from Objects.Items import ItemList, UnknownItem, UnknownArmour, ItemType, ArmourType, UnknownItemType, UnknownArmourType
from Objects.Sprites import MenuSprites


class Error(Exception): pass

class EmptyBag(Error): pass

class InvalidIndex(Error): pass

class NotInBag(Error): pass

class FullBag(Error): pass

class TooManySelections(Error): pass

class NoItem(Error): pass


class NoSelection(Error):
    def __init__(self, message="How stupid are you, read the docstrings"):
        super().__init__(message)
    

class ThisShouldntComeUp(Error):
    def __init__(self, message="How??!?"):
        super().__init__(message)


@dataclass(init=False)
class Armour:
    """Set player armour attributes
    :param helmet:"""
    helmet: Optional[ArmourType]
    chestplate: Optional[ArmourType]
    leggings: Optional[ArmourType]
    boots: Optional[ArmourType]
    ring1: Optional[ArmourType]
    ring2: Optional[ArmourType]


@dataclass(init=False)
class Weapons:
    """Set player weapon attributes"""
    weapon1: Optional[ItemType]
    weapon2: Optional[ItemType]
    quiver: int


@dataclass(init=False)
class Stats:
    """Set player stats attributes"""
    current_hp: int = field(init=False)
    hp: int
    dmg: int
    defence: int
    crit: int
    crit_chance: int
    block: int

    def __post_init__(self):
        self.current_hp = self.hp


@dataclass(init=False)
class Levels:
    """Set player level attributes"""
    difficulty: Optional[int] = None
    player_level: int = 1
    player_exp: int = 0

class InventoryBus:
    def __init__(self):
        self.listeners = {}

    def listen(self, event_name: str, callback: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, payload):
        for listener in self.listeners.get(event_name, []):
            if isinstance(payload, List):
                cargo: Optional[ItemType] = listener(*payload)
            else:
                cargo: Optional[ItemType] = listener(payload)
            if cargo is not None:
                return cargo


class InventoryState:
    def __init__(self, dev_mode: bool = False) -> None:
        self.dev_mode: bool = dev_mode

        self.exp_bar: Optional[int] = None
        self.required_exp_percent: int = 0
        self.required_exp: int = 0

        queue_max_size: int = 10
        self.weapon_bag: queue.Queue = queue.Queue(maxsize=queue_max_size)
        self.armour_bag: queue.Queue = queue.Queue(maxsize=queue_max_size)

        self.Armour: Armour = Armour()
        self.Weapons: Weapons = Weapons()
        self.Stats: Stats = Stats()
        self.Levels: Levels = Levels()

        self.armour_slots: list = ["helmet", "chestplate", "leggings", "boots", "ring1", "ring2"]
        self.weapon_slots: list = ["weapon1", "weapon2", "quiver"]
        self.stat_slots: list = ["hp", "dmg", "defence", "crit", "crit_chance", "block"]
        self.level_slots: list = ["difficulty", "player_level", "player_exp"]

    @property
    def armour_list(self) -> List[Union[ArmourType, UnknownArmourType]]:
        return [getattr(self.Armour, attribute) for attribute in self.armour_slots]

    @property
    def weapon_list(self) -> List[Union[ItemType, UnknownItemType]]:
        return [getattr(self.Weapons, attribute) for attribute in self.weapon_slots]

    @property
    def stat_list(self) -> List[int]:
        return [getattr(self.Stats, attribute) for attribute in self.stat_slots]

    def new_player(self) -> None:
        """give new player preset items"""
        [setattr(self.Armour, attribute, UnknownArmour())
         for attribute in self.armour_slots]
        [setattr(self.Weapons, attribute, UnknownItem()) if attribute != "quiver" else 
         setattr(self.Weapons, attribute, 0) for attribute in self.weapon_slots]
        [setattr(self.Stats, attribute, value)
         for attribute, value in zip(self.stat_slots, [10, 1, 0, 0, 0, 0])]
        [setattr(self.Levels, attribute, value)
         for attribute, value in zip(self.level_slots, [None, 1, 0])]
        self.Armour.ring1 = ItemList.wedding_ring
        self.Armour.helmet = ItemList.straw_sunhat
        self.Weapons.weapon1 = ItemList.basic_sword
        self.weapon_bag.put(ItemList.rock)


@dataclass
class InventoryPersistance:
    state: InventoryState
    bus: InventoryBus

    def __post_init__(self):
        signal_list = ("get_weapon_from_bag_with_weapon_name", "get_weapon_from_bag_with_index",
                       "unequip_weapon_with_weapon_name", "unequip_weapon_with_index",
                       "equip_weapon", "drop_weapon")
        for signal in signal_list:
            function = getattr(self, signal)
            self.bus.listen(signal, function)

    def save_player(self) -> None:
        """Set armour/weapons/stats/levels/bag to dicts and dump to JSON"""
        arm, wep, stat, lev = self.state.Armour, self.state.Weapons, self.state.Stats, self.state.Levels
        armour_dict = {"Helmet": arm.helmet, "Chestplate": arm.chestplate, "Leggings": arm.leggings,
                       "Boots": arm.boots, "Ring1": arm.ring1, "Ring2": arm.ring2}
        weapon_dict = {"Weapon1": wep.weapon1,
                       "Weapon2": wep.weapon2, "Quiver": wep.quiver}
        stat_dict = {"Hp": stat.hp, "Dmg": stat.dmg, "Defence": stat.defence, "Crit": stat.crit,
                     "Block": stat.block}
        level_dict = {"Difficulty": lev.difficulty,
                      "Player Level": lev.player_level}
        bag = []
        bag_queue = self.bag

        for _ in range(bag_queue.qsize()):
            item = bag_queue.get()
            hidden = item.hidden.hidden_template
            item = item.item_template
            item["Hidden"] = hidden
            bag.append(item)

        dicts = [("weapon", weapon_dict), ("armour", armour_dict)]

        for subdict in dicts:

            for key, value in subdict[1].items():

                if value is not None and key != "Quiver":
                    hidden = value.hidden.hidden_template

                    if subdict[0] == "weapon":
                        item = value.item_template

                    else:
                        item = value.armour_template

                    item["Hidden"] = hidden
                    subdict[1][key] = item

        with open("character.json", "w") as f:
            player = {"Armour": armour_dict, "Weapons": weapon_dict, "Bag": bag,
                      "Stats": stat_dict, "Levels": level_dict}
            json.dump(player, f, indent=2)
            f.close()
            print("Success!")

        return None

    def load_player(self) -> None:
        with open("character.json", "r") as f:
            player = json.load(f)
            f.close()

        player_dict_keys = ["Weapons", "Armour"]
        player_dicts = [player[key] for key in player_dict_keys]

        for subdict in player_dicts:

            dict_keys = player_dict_keys[player_dicts.index(subdict)]

            for key, value in subdict.items():

                if value is not None and key != "Quiver":
                    key = key.lower()
                    value = value["Name"].lower().replace(" ", "_")
                    exec(f"self.state.{dict_keys}.{key} = ItemList.{value}")

        self.state.Weapons.quiver = player["Weapons"]["Quiver"]

        stats = player["Stats"]

        for key, value in stats.items():
            setattr(self.state.Stats, str(value),
                    getattr(self.state.Stats, key.lower()))

        items = player["Bag"]
        player_bag = queue.Queue(maxsize=10)

        for item in items:
            item_name = item["Name"].lower().replace(" ", "_")
            item = getattr(ItemList, item_name)
            player_bag.put(item)

        self.bag = player_bag

        print("Success!")

        return None

    def equip_weapon(self, weapon_name: Optional[str], index: Optional[int]) -> None:        
        if weapon_name is None and index is None:
            raise NoSelection
        
        elif weapon_name is not None:
            item = self.get_weapon_from_bag_with_weapon_name(weapon_name=weapon_name, copy=False)

        elif index is not None:
            item = self.get_weapon_from_bag_with_index(index=index, copy=False)

        else:
            raise TooManySelections
        
        item_weight, weapon_slot_1_weight, weapon_slot_2_weight = None, None, None
        weapon1 = self.state.Weapons.weapon1
        weapon2 = self.state.Weapons.weapon2
        size = self.state.weapon_bag.qsize()

        item_name = item.name
        item_weight = item.item_weight
        weapon1 = self.state.Weapons.weapon1
        weapon_slot_1_name = weapon1.name
        weapon_slot_1_weight = weapon1.item_weight
        weapon2 = self.state.Weapons.weapon2
        weapon_slot_2_name = weapon2.name
        weapon_slot_2_weight = weapon2.item_weight

        if item_weight == 1 and (weapon_slot_1_weight == 0 or weapon_slot_2_weight == 0):
            slot = "weapon1" if weapon_slot_1_weight == 0 else "weapon2"
            setattr(self.state.Weapons, slot, item)
        
        elif item_weight == 1 and (weapon_slot_1_weight != 0 and weapon_slot_1_weight != 0):
            print(f"Which weapon would you like to replace?: \n \
                   \r 1) Weapon 1 - {weapon_slot_1_name} \n \
                   \r 2) Weapon 2 - {weapon_slot_2_name} \n \
                   \r 3) Cancel \n")

            while (selection := input(">").lower().replace(" ", "")) not in \
                ("weapon1", "weapon2", "cancel", weapon_slot_1_name, weapon_slot_2_name, "1", "2", "3"):
                print("Invalid selection\n")

            if selection in ("weapon1", weapon_slot_1_name, "1"):
                slot = "weapon1"
                to_replace = getattr(self.state.Weapons, "weapon1")


            elif selection in ("weapon2", weapon_slot_2_name, "2"):
                slot = "weapon2"
                to_replace = getattr(self.state.Weapons, "weapon2")

            elif selection in ("cancel", "3"):
                slot = None
                to_replace = item
            
            else:
                raise ThisShouldntComeUp

            if slot is not None:
                setattr(self.state.Weapons, slot, item)
            self.state.weapon_bag.put(to_replace)
        
        elif item_weight == 2 and (weapon_slot_1_weight == 0 and weapon_slot_2_weight == 0):
            if size > 8:
                raise FullBag
            setattr(self.state.Weapons, "weapon1", item)

        elif item_weight == 2 and (weapon_slot_1_weight != 0 or weapon_slot_1_weight != 0):
            while (selection := input(f"Would you like to replace both your weapons with \
                {item_name}\n").lower()) not in ('y', "yes", 'n', "no"):
                print("Invalid selection")

            if selection in ('n', "no"):
                self.state.weapon_bag.put(item)

            elif selection in ('y', "yes"):
                if size > 8:
                    raise FullBag
                with suppress(AttributeError):
                    item1 = getattr(self.state.Weapons, "weapon1")
                    item2 = getattr(self.state.Weapons, "weapon2")
                setattr(self.state.Weapons, "weapon1", item)
                self.state.weapon_bag.put(item1)
                self.state.weapon_bag.put(item2)

            else:
                self.state.weapon_bag.put(item)
                raise ThisShouldntComeUp

    def get_weapon_from_bag_with_weapon_name(self, weapon_name: str, copy: bool) -> ItemType:
        bag_item = None
        bag_size = self.state.weapon_bag.qsize()

        if weapon_name is None:
            raise NoSelection

        if bag_size == 0:
            raise EmptyBag

        bag_item = self.state.weapon_bag.get()

        while bag_item.name.lower() != weapon_name and bag_size > 0:
            self.state.weapon_bag.put(bag_item)
            bag_item = self.state.weapon_bag.get()
            bag_size -= 1

        if bag_size == 0 and bag_item.name.lower() != weapon_name:
            self.state.weapon_bag.put(bag_item)
            raise NotInBag

        if copy and bag_item is not None:
            bag_item_temp = bag_item
            self.state.weapon_bag.put(bag_item_temp)

        return bag_item

    def get_weapon_from_bag_with_index(self, index: int, copy: bool) -> ItemType:
        bag_item = None
        bag_size = self.state.weapon_bag.qsize()

        if index is None:
            raise NoSelection

        if bag_size == 0:
            raise EmptyBag

        if index > bag_size:
            raise InvalidIndex

        bag_item = self.state.weapon_bag.get()

        while index >= 1:
            self.state.weapon_bag.put(bag_item)
            bag_item = self.state.weapon_bag.get()
            index -= 1

        if copy and bag_item is not None:
            bag_item_temp = bag_item
            self.state.weapon_bag.put(bag_item_temp)

        return bag_item

    def unequip_weapon_with_weapon_name(self, weapon_name: str) -> None:
        if weapon_name is None:
            raise NoSelection

        if self.state.weapon_bag.full():
            raise FullBag

        if weapon_name is not None:
            for weapon_slot in self.state.weapon_slots:
                selected_item = getattr(self.state.Weapons, weapon_slot)
                print(selected_item)
                if selected_item.name == None:
                    pass
                elif selected_item.name.lower().replace(" ", "").replace("-", "") == weapon_name:
                    setattr(self.state.Weapons, weapon_slot, UnknownItem())
                    self.state.weapon_bag.put(selected_item)
                    return None
            else:
                raise NotInBag

    def unequip_weapon_with_index(self, index: str) -> None:
        if index is None:
            raise NoSelection

        if self.state.weapon_bag.full():
            raise FullBag
        
        if index is not None and index in ["weapon1", "weapon2"]:
            selected_item = getattr(self.state.Weapons, index)

            if isinstance(selected_item, UnknownItem):
                raise NoItem

            setattr(self.state.Weapons, index, UnknownItem())
            self.state.weapon_bag.put(selected_item)
            return None
        else:
            raise InvalidIndex

    @overload
    def drop_weapon(self, weapon_name: str, index: Literal[None]) -> None:
        ...

    @overload
    def drop_weapon(self, weapon_name: Literal[None], index: int) -> None:
        ...

    def drop_weapon(self, weapon_name: Optional[str], index: Optional[int]) -> None:
        selected_item = None

        if weapon_name is not None and index is not None:
            raise NoSelection

        elif weapon_name is not None:
            selected_item = self.get_weapon_from_bag_with_weapon_name(weapon_name=weapon_name, copy=False)

        elif index is not None:
            selected_item = self.get_weapon_from_bag_with_index(index=index, copy=False)

        input_message = f"Do you want to drop {weapon_name}? This cannot be undone: "

        while (selection := input(input_message)) not in ('y', "yes", 'n', "no"):
            print("Invalid selection [y/n]")

        if selection in ["n", "no"]:
            self.state.weapon_bag.put(selected_item)
            print(f"{weapon_name} has been returned to your bag")

        elif selection in ["y", "yes"]:
            print(f"{weapon_name} has been dropped")

        return None


@dataclass
class InventoryDisplay:
    state: InventoryState
    bus: InventoryBus

    def stats_setup(self, in_loop: bool) -> Tuple[List, int]:
        """
        :return: [hp, armour_hp, dmg, weapon_dmg, defence, armour_defence, crit, weapon_crit, crit_chance,
                  weapon_crit_chance, block, self.Levels.player_level, exp, exp_percent]
        """

        def exp() -> Tuple[float, float, int]:
            level_with_decimal = (
                ((100 * (2 * self.state.Levels.player_exp + 25)) ** (1 / 2)) + 50) / 100
            level_int = int(level_with_decimal)
            next_level = level_int + 1
            next_level_exp = (next_level ** 2 + next_level) / \
                2 * 100 - (next_level * 100)

            required_exp = next_level_exp - self.state.Levels.player_exp
            required_exp_percent = required_exp / next_level_exp * 100

            return required_exp, required_exp_percent, level_int

        hp, dmg, defence, crit, crit_chance, block = self.state.stat_list
        armour_hp, armour_defence = 0, 0
        weapon_dmg, weapon_crit, weapon_crit_chance = 0, 0, 0

        armour_list = self.state.armour_list
        for armour in armour_list:

            try:
                armour_hp += armour.hp
                armour_defence += armour.defence

            except AttributeError:
                pass

        for weapon in self.state.weapon_list:

            try:
                weapon_dmg += weapon.dmg
                weapon_crit += weapon.crit
                weapon_crit_chance += weapon.crit_chance

            except AttributeError:
                pass

        current_exp, exp_percent, level = exp()
        setattr(self.state.Levels, "player_level", level)
        self.stat_list_temp = [hp, armour_hp, dmg, weapon_dmg, defence, armour_defence, crit, weapon_crit, crit_chance,
                               weapon_crit_chance, block, self.state.Levels.player_level, exp, exp_percent]

        if in_loop:
            current_hp = self.state.Stats.current_hp
            return self.stat_list_temp, current_hp

        else:
            return self.stat_list_temp, 0

    def inventory_display(self) -> None:  # class
        """Displays with setup"""
        armour_display = MenuSprites.InventoryMenus.inventory_armour_menu
        weapon_display = MenuSprites.InventoryMenus.inventory_weapon_menu
        bag_display = MenuSprites.InventoryMenus.inventory_bag_menu

        def armour_menu() -> None:
            """Display for armour"""
            armour_list = []
            for armour in self.state.armour_list:
                if armour is None:
                    armour = UnknownArmour()
                    armour_list.append(armour)
                else:
                    armour_list.append(armour)
            

            print(armour_display(armour_list=armour_list))
            input_message = "1) Select Item, 2) Next Page, 3) Exit\n"

            while (selection := input(input_message)) not in ("1", "2", "3"):
                print(f"Invalid Selection: {selection}")

            if selection == "1":
                armour_selection = input("Selection: ").lower()
                armour_selection_list = ("helmet", "chestplate", "leggings", "boots", "ring1", "ring2")

                if armour_selection.replace(" ", "") in armour_selection_list:
                    armour = getattr(self.state.Armour, armour_selection)
                    print(MenuSprites.InventoryMenus.armour_selection(armour))

                else:
                    _armour_selection = armour_selection.title()
                    armour_list_names = [armour.name for armour in armour_list]

                    if _armour_selection in armour_list_names:
                        index = armour_list_names.index(_armour_selection)
                        print(MenuSprites.InventoryMenus.armour_selection(armour_list[index]))

                    else:
                        print(f"Invalid selection: {armour_selection}")

                armour_menu()

            elif selection == "2":
                weapon_menu()

            elif selection == "3":
                return None

        def weapon_menu() -> None:
            """Display for weapon slots + quiver"""
            weapon_list = []

            for weapon in self.state.weapon_list:
                if weapon is None:
                    weapon = UnknownItem()
                    weapon_list.append(weapon)
                else:
                    weapon_list.append(weapon)
            
            print(weapon_display(weapon_list=weapon_list))
            input_message = "1) Select Item, 2) Unequip Weapon 3) Next Page 4) Previous Page, 5) Exit\n"

            while (selection := input(input_message)) not in ("1", "2", "3", "4", "5"):
                print(f"Invalid Selection: {selection}")

            if selection == "1":
                weapon_selection = input("Selection: ").lower().replace(" ", "_")

                if weapon_selection.replace("_", "") in ("weapon1", "weapon2"):
                    weapon = getattr(self.state.Weapons, weapon_selection)
                    print(MenuSprites.InventoryMenus.weapon_selection(weapon))

                else:
                    weapon_selection = weapon_selection.title()
                    print(weapon_list)
                    weapon_list_names = [weapon for weapon in weapon_list]

                    if weapon_selection in weapon_list_names:
                        index = weapon_list_names.index(weapon_selection)
                        print(MenuSprites.InventoryMenus.weapon_selection(weapon_list[index]))

                    else:
                        print(f"Invalid selection: {weapon_selection}")

                weapon_menu()

            elif selection == "2":
                weapon_selection = input(
                    "Which weapon would you like to unequip?\n").lower().replace(" ", "")

                if weapon_selection in ("1", "2"):
                    weapon_selection = f"weapon{weapon_selection}"

                try:
                    if weapon_selection in ("weapon1", "weapon2"):
                        self.bus.emit("unequip_weapon_with_index", weapon_selection)

                    else:
                        self.bus.emit("unequip_weapon_with_weapon_name", weapon_selection)

                except FullBag:
                    print("Your bag is full")

                except (NotInBag, InvalidIndex) as _:
                    print(f"Invalid selection: {weapon_selection}")

                except NoItem:
                    print("There's nothing to unequip in that slot")

                weapon_menu()

            elif selection == "3":
                bag_menu()

            elif selection == "4":
                armour_menu()

            elif selection == "5":
                return None

        def bag_menu() -> None:
            bag_list: List[Union[ItemType, UnknownItemType]] = []

            for index in range(1, 11):
                try:
                    item: Optional[Union[ItemType, UnknownItemType]] = \
                        self.bus.emit("get_weapon_from_bag_with_index", [index, True])

                    if item == None:
                        raise ThisShouldntComeUp

                    bag_list.append(item)

                except NoSelection:
                    raise NoSelection

                except EmptyBag:
                    item = UnknownItem()
                    bag_list.append(item)
                    
                except InvalidIndex:
                    item = UnknownItem()
                    bag_list.append(item)

            print(bag_display(bag_list))

            input_message = "1) Select Item, 2) Equip Weapon, 3) Drop Weapon 4) Previous Page, 5) Exit\n"
            
            while (selection := input(input_message)) not in ("1", "2", "3", "4", "5"):
                print("Invalid Selection")

            if selection == "1":
                weapon_selection = input("Selection: ").lower().replace(" ", "_")

                try:
                    if weapon_selection in [str(number) for number in range(1, 11)]:
                        index = int(weapon_selection)
                        item = self.bus.emit("get_weapon_from_bag_with_index", [index, True])

                    else:
                        item = self.bus.emit("get_weapon_from_bag_with_weapon_name", [weapon_selection, True])
                    
                    if item is None:
                        raise ThisShouldntComeUp

                    print(MenuSprites.InventoryMenus.weapon_selection(item))

                except EmptyBag:
                    print("There's nothing to select")

                except (NotInBag, InvalidIndex) as e:
                    if e == NotInBag:
                        print(f"Invalid selection: {weapon_selection}")

                    elif e == InvalidIndex:
                        print(f"Bag index {weapon_selection} is invalid")

                bag_menu()

            elif selection == "2":
                weapon_selection = input("Which weapon would you like to equip?\n").lower()

                try:
                    if weapon_selection in [str(number) for number in range(1, 11)]:
                        self.bus.emit("equip_weapon", [None, int(weapon_selection)])

                    else:
                        self.bus.emit("equip_weapon", [weapon_selection, None])

                except EmptyBag:
                    print("There's nothing to equip")

                except (NotInBag, InvalidIndex) as e:
                    if e == NotInBag:
                        print(f"Invalid selection: {weapon_selection}")
                    
                    elif e == InvalidIndex:
                        print(f"Bag index {weapon_selection} is invalid")

                bag_menu()

            elif selection == "3":
                weapon_selection = input(
                    "Which weapon would you like to drop?\n").lower()

                try:
                    if weapon_selection in [str(number) for number in range(1, 11)]:
                        self.bus.emit("drop_weapon", [None, int(weapon_selection)])

                    else:
                        self.bus.emit("drop_weapon", [weapon_selection, None])

                except EmptyBag:
                    print("There's nothing to drop")

                except (NotInBag, InvalidIndex) as e:
                    if e == NotInBag:
                        print(f"Invalid selection {weapon_selection}")

                    elif e == InvalidIndex:
                        print(f"Bag index {weapon_selection} is invalid")

                bag_menu()

            elif selection == "4":
                weapon_menu()

            elif selection == "5":
                return None

        armour_menu()

    def stats_display(self, in_loop: bool):
        """Setup and display player stats + armour/weapon stats"""
        stats_list, current_hp = self.stats_setup(in_loop)
        stat_display = MenuSprites.InventoryMenus.stats_menu(
            stats_list, current_hp)
        print(stat_display)
        return None


class Inventory:
    def __init__(self, state: InventoryState, bus: InventoryBus) -> None:
        self.state = state
        self.persistance = InventoryPersistance(state, bus)
        self.display = InventoryDisplay(state, bus)

    def save(self):
        self.persistance.save_player()

    def load(self):
        self.persistance.load_player()
