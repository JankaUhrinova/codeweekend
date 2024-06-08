import json
from world import Action, Hero, Monster, World


def read_input(filename: str):
    with open(filename) as f:
        info = json.load(f)

    # Hero initialization
    hero_info = info["hero"]
    h_x = info["start_x"]
    h_y = info["start_y"]
    h_speed = hero_info["base_speed"]
    h_power = hero_info["base_power"]
    h_range = hero_info["base_range"]
    s_c = hero_info["level_speed_coeff"]
    p_c = hero_info["level_power_coeff"]
    r_c = hero_info["level_range_coeff"]

    hero = Hero(h_x, h_y, h_speed, h_power, h_range, s_c, p_c, r_c)

    # Monsters initialization
    monsters = []
    monsters_info = info["monsters"]
    for id, m in enumerate(monsters_info):
        m_x = m["x"]
        m_y = m["y"]
        m_hp = m["hp"]
        m_gold = m["gold"]
        m_exp = m["exp"]

        monster = Monster(m_x, m_y, m_hp, m_gold, m_exp, id)
        monsters.append(monster)

    # World initialization
    w_height = info["height"]
    w_width = info["width"]
    w_turns = info["num_turns"]
    world = World(w_height, w_width, hero, monsters, w_turns)

    return world


def print_output(filename: str, actions: list[Action]):

    with open(filename, "w+") as f:
        json.dump({"moves": actions}, f, indent=4, default=vars)
