class Hero():
    def __init__(self, x : int, y : int, base_speed: int, base_power: int,
                base_range: int, speed_coef: int, power_coef: int, range_coef: int):
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

class Monster():
    def __init__(self, x : int,y : int, hp: int, gold: int, xp: int):
        self.x = x
        self.y = y
        self.hp = hp
        self.gold = gold
        self.xp = xp

class World():
    def __init__(self, height : int, width : int, hero: Hero, monsters: list[Monster], turns: int):
        self.height = height
        self.width = width
        self.hero = hero
        self.monsters = monsters    
        self.turns = turns

        