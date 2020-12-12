from typing import Union, List, Optional

from Objects.Items import UnknownWeaponType, WeaponType
from InventorySystem import Inventory, ThisShouldntComeUp
from Objects.Sprites import MenuSprites


class ShopMenu:
    def __init__(self, inv: Inventory) -> None:
        self.inv = inv
        self.state = inv.state
        self.bus = self.inv.bus
        self.balance = self.inv.state.Levels.balance

        self.weapons = self.state.weapon_list
        self.armour = self.state.armour_list

        self.shop_menu()

    
    def shop_menu(self):
        print(MenuSprites.ShopMenus.shop_menu(self.balance))
        while (selection := input("Selection - ").lower()) not in \
        ("1", "buy" "2", "sell", "3", "inventory", "inv"):
            print("Invalid Selection")

        if selection in ("1", "buy"):
            pass

        elif selection in ("2", "sell"):
            self.sell_weapon()

        elif selection in ("3", "inventory", "inv"):
            self.bus.emit("inventory_display", None)
            self.shop_menu()

    def sell_weapon(self):
        weapon_list: List[Union[WeaponType, UnknownWeaponType]] = self.weapons
        weapon_list = weapon_list[:-1]
        for index in range(0, self.state.weapon_bag.qsize()):
            weapon: Optional[Union[WeaponType, UnknownWeaponType]] = \
                self.bus.emit("get_weapon_from_bag_with_index",
                              [index, True])

            if weapon == None:
                raise ThisShouldntComeUp

            weapon_list.append(weapon)

        print(MenuSprites.ShopMenus.shop_menu_sell("weapons", weapon_list))
        
        
            