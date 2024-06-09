from math import floor, copysign
import sys

from code.world import Action, Attack, Move, World
from code.utils import (
    hits_needed,
    steps_to_reach_cca,
    in_attack_range,
    attack,
    clamp_hero_position_to_world,
    jump_towards_monster,
)
from code.input_output import read_input, write_output


def sign(x):
    return copysign(1, x)


def solve(world: World) -> list[Action]:

    result: list[Action] = []

    monsters = world.monsters[:]
    t = world.turns
    h = world.hero

    while t > 0 and len(monsters):

        t -= 1

        if t % 100 == 0:
            print(f"{t} turns left")

        monsters.sort(key=lambda m: -(hits_needed(h, m) + steps_to_reach_cca(h, m)))
        m = monsters[-1]

        if in_attack_range(h, m):
            result.append(Attack(m.id))

            killed = attack(h, m)
            if killed:
                monsters.pop()

            continue

        # treba skocit :o no ale kam juj
        move = jump_towards_monster(h, m)

        h.x = move.target_x
        h.y = move.target_y
        clamp_hero_position_to_world(h, world)

        result.append(Move(h.x, h.y))

    return result


if __name__ == "__main__":

    f = sys.argv[1]
    o = sys.argv[2]

    world = read_input(f)

    result = solve(world)

    print(world.hero.gold)

    write_output(o, result)
