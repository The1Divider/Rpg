from dataclasses import dataclass

from Objects.Sprites import EnemySprites as Es
from Objects.Sprites import EnemySpriteType

"""
@dataclass
class Enemy:
    name: str
    passive_sprite: EnemySpriteType
    aggro_sprite: EnemySpriteType
    level: int
    level_cap: int

    hp: int
    dmg: int
    defence: int
    block: int
"""


@dataclass
class Rat:
    name: str = "Rat"
    passive_sprite: EnemySpriteType = Es.rat_passive
    aggro_sprite: EnemySpriteType = Es.rat_aggressive
    level: int = 1
    level_cap: int = 5

    hp: int = 5
    dmg: int = 1
    defence: int = 0
    block: int = 0
