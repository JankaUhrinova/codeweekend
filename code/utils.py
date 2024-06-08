from math import ceil

from world import Hero, Monster


def hits_needed(hero: Hero, monster: Monster) -> int:
    return ceil(monster.hp / hero.power)
