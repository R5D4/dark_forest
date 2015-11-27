""" Contains data used by tests."""

# 1H, equip in R_hand, no stat requirements
TESTING_KNIFE = {
           'name': 'Testing Knife',
           'class': 'knife',
           'rarity': 0,
           'slot': ['R_hand'],
           'atk_type': 'pierce',
           'attribute': 'dex',
           'require': {'str': 0, 'dex': 0},
           'bonus': {'str': 0, 'dex': 10, 'AC': 0},
           'dmg_roll': '1d6',
           'description': "For testing only!"
           }
# 1H, equip in R_hand
TESTING_SWORD = {
           'name': 'Testing Sword',
           'class': '1h_sword',
           'rarity': 0,
           'slot': ['R_hand'],
           'atk_type': 'slash',
           'attribute': 'str',
           'require': {'str': 5, 'dex': 5},
           'bonus': {'str': 10, 'dex': 0, 'AC': 0},
           'dmg_roll': '1d8',
           'description': "For testing only!"
           }
# 1H, equip in L_hand
TESTING_SHIELD = {
           'name': 'Testing Shield',
           'class': 'shield',
           'rarity': 0,
           'slot': ['L_hand'],
           'atk_type': 'blunt',
           'attribute': 'str',
           'require': {'str': 10, 'dex': 0},
           'bonus': {'str': 0, 'dex': -10, 'AC': 20},
           'dmg_roll': '1d4',
           'description': "For testing only!"
           }
# 2H, equip in both R_hand and L_hand
TESTING_BOW = {
           'name': 'Testing Bow',
           'class': 'bow',
           'rarity': 0,
           'slot': ['R_hand', 'L_hand'],
           'atk_type': 'pierce',
           'attribute': 'dex',
           'require': {'str': 0, 'dex': 10},
           'bonus': {'str': 0, 'dex': 10, 'AC': 0},
           'dmg_roll': '1d8',
           'description': "For testing only!"
           }

