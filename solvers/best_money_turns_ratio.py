import os
from code.input_output import read_input, write_output
from code.world import Action, Attack, Move, World
from code.utils import (
    hits_needed,
    steps_to_reach_cca,
    in_attack_range,
    attack,
    clamp_hero_position_to_world,
    jump_towards_monster,
)
from math import ceil

def solve(world: World) -> list[Action]:
    result: list[Action] = []

    monsters = world.monsters
    hero = world.hero
    turns = world.turns

    while(turns > 0):
        priorities: list[(float, int)] = []
        for i, monster in enumerate(monsters):
            turns_for_kill = hits_needed(hero, monster) + steps_to_reach_cca(hero, monster)
            if(turns_for_kill <= turns):
                priority = turns_for_kill/monster.gold
                priorities.append((priority, i))
        priorities.sort()
        if(len(priorities) == 0):
            break
        chosen = monsters[priorities[0][1]]

        while(not in_attack_range(hero, chosen)):
            move = jump_towards_monster(hero, chosen)
            hero.x = move.target_x
            hero.y = move.target_y
            clamp_hero_position_to_world(hero, world)

            result.append(Move(hero.x, hero.y))
            turns -= 1
        
        while(chosen.is_alive):
            attack(hero, chosen)
            result.append(Attack(chosen.id))
            turns -= 1

        monsters.remove(chosen)
        
    return result
