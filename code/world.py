from dataclasses import dataclass
from memoization import cached
from math import floor
from typing import Union


@dataclass
class Move:
    target_x: int
    target_y: int
    comment: str = ""
    type: str = "move"


@dataclass
class Attack:
    target_id: int
    comment: str = ""
    type: str = "attack"


Action = Union[Move, Attack]


class Hero:
    def __init__(
        self,
        x: int,
        y: int,
        base_speed: int,
        base_power: int,
        base_range: int,
        speed_coef: int,
        power_coef: int,
        range_coef: int,
    ):
        self.x = x
        self.y = y
        self.base_speed = base_speed
        self.base_power = base_power
        self.base_range = base_range
        self.speed_coef = speed_coef
        self.power_coef = power_coef
        self.range_coef = range_coef
        self.xp = 0
        self.gold = 0

        self._level = 0

    # For level L, an additional 1000 + L ⋅ (L − 1) ⋅ 50 experience points are required
    # after reaching the previous level.
    @cached
    @staticmethod
    def level_xp(level: int) -> int:
        if level == 0:
            return 0

        return Hero.level_xp(level - 1) + 1000 + level * (level - 1) * 50

    @property
    def xp_needed(self) -> int:
        return Hero.level_xp(self.level + 1) - self.xp

    @property
    def level(self) -> int:
        while self.xp >= Hero.level_xp(self._level + 1):
            self._level += 1
        return self._level

    # moves with a speed of ⌊ base_speed ⋅ (1 + L ⋅ level_speed_coeff / 100) ⌋
    @property
    def speed(self) -> int:
        return floor(self.base_speed * (1 + self.level * self.speed_coef / 100))

    # attacks with a power of ⌊ base_power ⋅ (1 + L ⋅ level_power_coeff / 100 ) ⌋
    @property
    def power(self) -> int:
        return floor(self.base_power * (1 + self.level * self.power_coef / 100))

    # has an attack range of ⌊ base_range ⋅ (1 + L ⋅ level_range_coeff / 100 ) ⌋
    @property
    def attack_range(self) -> int:
        return floor(self.base_range * (1 + self.level * self.range_coef / 100))


class Monster:
    def __init__(self, x: int, y: int, hp: int, gold: int, xp: int, id: int):
        self.x = x
        self.y = y
        self.hp = hp
        self.gold = gold
        self.xp = xp
        self.id = id

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    @property
    def is_dead(self) -> bool:
        return not self.is_alive


class World:
    def __init__(
        self, height: int, width: int, hero: Hero, monsters: list[Monster], turns: int
    ):
        self.height = height
        self.width = width
        self.hero = hero
        self.monsters = monsters
        self.turns = turns
