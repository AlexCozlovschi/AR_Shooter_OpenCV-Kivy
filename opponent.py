import Stats


class Opponent:
    def __init__(self, hp, damage, armor):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def attac(self, harm):
        if self.hp > 0:
            self.hp = self.hp - harm
        else:
            print('death')


enemy = Opponent(0, 0, 0)


def target_detection():
    if Stats.x in range(Stats.posi[0], Stats.posi[0] + Stats.posi[1]):
        if Stats.y in range(Stats.posi[2], Stats.posi[2] + Stats.posi[3]):
            if Stats.Bullet > 0:
                enemy.attac(10)


def slime():
    global enemy
    hp = 100
    damage = 5
    armor = 0
    enemy = Opponent(hp, damage, armor)


def knight():
    global enemy
    hp = 100
    damage = 10
    armor = 20
    enemy = Opponent(hp, damage, armor)


def boss():
    global enemy
    hp = 200
    damage = 10
    armor = 0
    enemy = Opponent(hp, damage, armor)


if Stats.enemy_type == 0:
    enemy = Opponent(0, 0, 0)
elif Stats.enemy_type == 1:
    slime()
elif Stats.enemy_type == 2:
    knight()
elif Stats.enemy_type == 3:
    boss()






