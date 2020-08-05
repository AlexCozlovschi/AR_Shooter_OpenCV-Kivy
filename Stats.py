# Player's Stats
hp_player = 200
Armor = 0
armor_player = 0
damage_player = 10
Bullet = 5
T_Bullet = 60

# Game Variables
alpha = 0.1
Bullet_show = 100
x = 0
y = 0
posi = [0, 0, 0, 0]
image = 0
enemy_type = 1


# Give HP
def HPBox():
    global hp_player
    if hp_player > 0:
        if hp_player + 10 > 200:
            hp_player = 200
        else:
            hp_player = hp_player + 10


# Give Bullets
def BulletBox():
    global T_Bullet
    if T_Bullet < 25:
        if T_Bullet + 5 > 25:
            T_Bullet = 25
        else:
            T_Bullet = T_Bullet + 5


def reload():
    global Bullet, T_Bullet
    if T_Bullet > 0:
        Bullet = 5


def Box(type):
    global image, enemy_type
    if type == "b'Boss'":
        image = 1
        enemy_type = 3
    elif type == "b'Mob'":
        image = 2
        enemy_type = 1
    elif type == "b'HPBox'":
        image = 3
        HPBox()

    elif type == "b'Bulet'":
        image = 4
        reload()


