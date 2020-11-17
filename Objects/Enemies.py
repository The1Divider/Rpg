from dataclasses import dataclass

from Objects.Sprites import EnemySprites as Es
from Objects.Sprites import EnemySpriteType


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


@dataclass
class Rat(Enemy):
    name = "Rat"
    passive_sprite = Es.rat_passive
    aggro_sprite = Es.rat_aggressive
    level = 1
    level_cap = 5

    hp = 5
    dmg = 1
    defence = 0
    block = 0
