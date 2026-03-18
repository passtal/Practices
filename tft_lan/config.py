"""TFT 시즌3 갤럭시 LAN - 게임 설정"""

PORT = 8080
MAX_PLAYERS = 4
MIN_PLAYERS = 2
PREP_TIME = 30
BOARD_ROWS = 4
BOARD_COLS = 7
BENCH_SIZE = 9
SHOP_SIZE = 5
MAX_LEVEL = 9
STARTING_HP = 100
STARTING_GOLD = 0
LEVEL_UP_COST = 4
LEVEL_UP_XP = 4
REFRESH_COST = 2
MAX_ITEMS_PER_UNIT = 3
STAR_UPGRADE_COUNT = 3
MAX_STARS = 3
PVE_ROUNDS = 3
AUGMENT_ROUNDS = [4, 12, 20]

LEVEL_UNIT_CAP = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
LEVEL_XP_REQUIRED = {2:2,3:6,4:10,5:20,6:36,7:56,8:80,9:100}
STAR_MULT = {1:1.0, 2:1.8, 3:3.24}
POOL_SIZE = {1:29, 2:22, 3:18, 4:12, 5:10}

SHOP_ODDS = {
    1:[1.00,0,0,0,0], 2:[1.00,0,0,0,0],
    3:[0.70,0.25,0.05,0,0], 4:[0.50,0.35,0.15,0,0],
    5:[0.37,0.35,0.25,0.03,0], 6:[0.24,0.35,0.30,0.10,0.01],
    7:[0.20,0.30,0.33,0.15,0.02], 8:[0.15,0.20,0.35,0.25,0.05],
    9:[0.10,0.15,0.30,0.30,0.15],
}

def calc_base_gold(rnd):
    if rnd<=1: return 2
    if rnd<=2: return 3
    if rnd<=3: return 4
    return 5

def calc_interest(gold):
    return min(gold//10, 5)

def calc_streak_gold(streak):
    s=abs(streak)
    if s>=5: return 3
    if s>=3: return 2
    if s>=2: return 1
    return 0
