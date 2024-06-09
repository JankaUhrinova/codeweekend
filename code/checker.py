from code.world import World, Action
from code.utils import dist_squared, in_attack_range, attack


# returns (score, error)
def check_and_score(world: World, actions: list[Action]) -> tuple[int, str]:
    if len(actions) > world.turns:
        return (
            0,
            f"Too many actions: world has {world.turns} but there are {len(actions)} actions",
        )

    for i, a in enumerate(actions):

        if a.type == "move":

            if (
                a.target_x < 0
                or a.target_x > world.width
                or a.target_y < 0
                or a.target_y > world.height
            ):
                return (
                    0,
                    f"Move {i} out of bounds: {a.target_x}, {a.target_y} not in [0, {world.width}], [0, {world.height}]",
                )

            jump_dist = dist_squared(
                (world.hero.x, world.hero.y), (a.target_x, a.target_y)
            )
            if jump_dist > world.hero.speed * world.hero.speed:
                return (
                    0,
                    f"Move {i} too long: from {world.hero.x}, {world.hero.y} to {a.target_x, a.target_y} is distance {jump_dist}, but hero range is {world.hero.speed * world.hero.speed}",
                )

            world.hero.x = a.target_x
            world.hero.y = a.target_y
        elif a.type == "attack":
            monster_id = a.target_id

            if monster_id < 0 or monster_id >= len(world.monsters):
                return (
                    0,
                    f"Invalid attack target {monster_id}: there are {len(world.monsters)} monsters",
                )

            if world.monsters[monster_id].is_dead:
                return (
                    0,
                    f"Invalid attack target {monster_id}: monster is already dead",
                )

            if not in_attack_range(world.hero, world.monsters[monster_id]):
                m = world.monsters[monster_id]
                dist = dist_squared((world.hero.x, world.hero.y), (m.x, m.y))
                range = world.hero.attack_range * world.hero.attack_range
                return (
                    0,
                    f"Monster out of range; attack from {world.hero.x},{world.hero.y} to {m.x},{m.y} has length {dist}, but range is {range}",
                )

            assert attack(world.hero, world.monsters[monster_id]) != -1
        else:
            return 0, f"Invalid action type: {a.type}"

    return world.hero.gold, ""
