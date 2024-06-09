from math import ceil, floor, copysign

from code.world import Hero, Monster, Move, World

# math stuff


def sign(x):
    return copysign(1, x)


def dist_squared(a: tuple[int, int], b: tuple[int, int]) -> int:
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])


# game stuff


def hits_needed(hero: Hero, monster: Monster) -> int:
    return ceil(monster.hp / hero.power)


def steps_to_reach_cca(hero: Hero, monster: Monster) -> int:

    dx = abs(monster.x - hero.x)
    dy = abs(monster.y - hero.y)

    # dx*dx + dy*dy - t*speed*speed* <= ar*ar
    # dx*dx + dy*dy - ar*ar <= t*speed*speed
    # (dx*dx + dy*dy - ar*ar) / (speed*speed) <= t

    dist = dx * dx + dy * dy
    dist -= hero.attack_range * hero.attack_range

    if dist <= 0:
        return 0

    if hero.speed == 0:
        return 123456789

    return ceil(dist / (hero.speed * hero.speed))


def in_attack_range(hero: Hero, monster: Monster) -> bool:
    return (
        dist_squared((hero.x, hero.y), (monster.x, monster.y))
        <= hero.attack_range * hero.attack_range
    )


# returns -1 if attack is not possible
# returns 0 if monster remains alive
# returns 1 if monster dies
# modifies hero and monster arguments
def attack(hero: Hero, monster: Monster) -> int:

    if not monster.is_alive or not in_attack_range(hero, monster):
        return -1

    monster.hp -= hero.power

    if monster.is_dead:
        hero.xp += monster.xp
        hero.gold += monster.gold

    return monster.is_dead


# returns true if clamp applied
def clamp_hero_position_to_world(hero: Hero, world: World) -> bool:
    clamped = hero.x < 0 or hero.x > world.width or hero.y < 0 or hero.y > world.height

    hero.x = max(hero.x, 0)
    hero.y = max(hero.y, 0)
    hero.x = min(hero.x, world.width)
    hero.y = min(hero.y, world.height)

    return clamped


# does not modify hero
def jump_towards_monster(hero: Hero, monster: Monster) -> Move:

    dx = monster.x - hero.x
    dy = monster.y - hero.y

    ratio = [abs(dx / (abs(dx) + abs(dy))), abs(dy / (abs(dx) + abs(dy)))]
    jump_dist = hero.speed * hero.speed

    cx, cy = ratio[0] * jump_dist, ratio[1] * jump_dist

    hopx = floor(cx**0.5)
    hopy = floor(cy**0.5)

    # if hopx * hopx + hopy * hopy > jump_dist:
    #     print(
    #         hero.x,
    #         hero.y,
    #         "trying to jump",
    #         dx,
    #         dy,
    #         "makes jump",
    #         hopx,
    #         hopy,
    #         "which is",
    #         hopx * hopx + hopy * hopy,
    #         "but can do",
    #         jump_dist,
    #         "with",
    #         hero.speed,
    #     )

    while hopx * hopx + hopy * hopy > jump_dist:
        if hopy > hopx:
            hopy -= 1
        else:
            hopx -= 1

    move = Move(hero.x + hopx * sign(dx), hero.y + hopy * sign(dy))

    # if we would jump over the monster, jump on top of it instead
    # (ideally we would jump as far in this direction as is useful, but I cannot math)
    if (
        dist_squared((hero.x, hero.y), (monster.x, monster.y))
        <= hero.speed * hero.speed
    ) and dist_squared(
        (move.target_x, move.target_y), (monster.x, monster.y)
    ) > hero.attack_range * hero.attack_range:
        return Move(monster.x, monster.y)

    return move
