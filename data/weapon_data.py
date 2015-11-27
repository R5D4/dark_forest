""" 
This module contains weapon descriptions.
"""
# weapon classes
#'2h_sword'
#'bastard_sword'
#'1h_sword'
#'knife'
#'axe'
#'bow'
#'shield'

# see data/attack_data.py for list of possible attack types

# huge array of dict objects specifying weapon characteristics
WEAPONS = [
    # New weapon template
    # {
    #   'name': <Weapon Name>
    #   'class': <Weapon Class>
    #   'rarity': <0-99 higher is rarer>
    #   'slot': <list of slot id strings>
    #   'atk_type': <weapon's attack type>
    #   'attribute': <the player attribute the weapon depends on>
    #   'require': <minimum base stats required to equip>
    #   'bonus': <weapon's stat bonuses>
    #   'dmg_roll': <weapon's dmg die>
    #   'description': <Flavour text description>
    # }
    {
    'name': 'Knight Sword',
    'class': 'bastard_sword',
    'rarity': 60,
    'slot': ['R_hand'],
    'atk_type': 'slash',
    'attribute': 'str',
    'require': {'str': 4, 'dex': 4},
    'bonus': {'str': 3, 'dex': 3, 'AC': 3},
    'dmg_roll': '1d8',
    'description': "A hand-and-a-half sword commonly used by men of Gondor.\
There are faint markings on the pommel depicting the tiered rings of Minas \
Tirith."
    },
    {
    'name': 'Elven Longbow',
    'class': 'bow',
    'rarity': 50,
    'slot': ['R_hand', 'L_hand'],
    'atk_type': 'pierce',
    'attribute': 'dex',
    'require': {'str': 2, 'dex': 5},
    'bonus': {'str': 0, 'dex': 5, 'AC': 1},
    'dmg_roll': '1d8',
    'description': "An elegant longbow made by one of the sylvan folk."
    },
    {
    'name': 'Hunting Knife',
    'class': 'knife',
    'rarity': 0,
    'slot': ['R_hand'],
    'atk_type': 'pierce',
    'attribute': 'dex',
    'require': {'str': 0, 'dex': 0},
    'bonus': {'str': 1, 'dex': 4, 'AC': 2},
    'dmg_roll': '1d6',
    'description': "A standard hunting knife. Simple but effective."
    },
    {
    'name': 'Knight Shield',
    'class': 'shield',
    'rarity': 90,
    'slot': ['L_hand'],
    'atk_type': 'blunt',
    'attribute': 'str',
    'require': {'str': 6, 'dex': 0},
    'bonus': {'str': 0, 'dex': -4, 'AC': 10},
    'dmg_roll': '1d4',
    'description': "A large sturdy shield almost as tall as you. The White \
Tree of Minath Tirith is painted on top of a black background."
    },
    {
    'name': 'Estoc',
    'class': '2h_sword',
    'rarity': 60,
    'slot': ['R_hand', 'L_hand'],
    'atk_type': 'pierce',
    'attribute': 'str',
    'require': {'str': 6, 'dex': 5},
    'bonus': {'str': 2, 'dex': 2, 'AC': 2},
    'dmg_roll': '1d10',
    'description': "A really long and straight sword. It's stiff and has no \
cutting edge. The blade comes to a fine point."
    },
    {
    'name': "Assassin's Dagger",
    'class': 'knife',
    'rarity': 80,
    'slot': ['R_hand'],
    'atk_type': 'pierce',
    'attribute': 'dex',
    'require': {'str': 0, 'dex': 8},
    'bonus': {'str': 0, 'dex': 0, 'AC': 0},
    'dmg_roll': '1d12',
    'description': "An enchanted dagger used for assassinations. It easily \
finds the heart of the target."
    },
#    {
#    'name': 'Long Sword',
#    'class': '2h_sword',
#    'attack': ['slash'],
#    'attribute': 'str',
#    'min_str': 5,
#    'min_dex': 3,
#    'hit_bonus': 2,
#    'dmg_roll': '1d8',
#    'dmg_bonus': 3,
#    'AC_bonus': ('parry', 3),
#    'description': "It's a long... sword. The blade is straight and double-\
#edged."
#    },
]

# Currently not available to the user
BOSS_WEAPONS = [
    {
    'name': 'Tusks',
    'class': 'head',
    'rarity': 0,
    'atk_type': 'pierce',
    'attribute': 'str',
    'require': {'str': 0, 'dex': 0},
    'bonus': {'str': 3, 'dex': 0, 'AC': 0},
    'dmg_roll': '1d8',
    'description': "A pair of sharp tusks made of animal bone."
    },
    {
    'name': 'Hooves',
    'class': 'feet',
    'rarity': 0,
    'atk_type': 'blunt',
    'attribute': 'str',
    'require': {'str': 0, 'dex': 0},
    'bonus': {'str': 2, 'dex': 2, 'AC': 0},
    'dmg_roll': '1d8',
    'description': "Some strong hooves."
    },
    {
    'name': 'Teeth',
    'class': 'head',
    'rarity': 0,
    'atk_type': 'pierce',
    'attribute': 'str',
    'require': {'str': 0, 'dex': 0},
    'bonus': {'str': 1, 'dex': 0, 'AC': 0},
    'dmg_roll': '1d6',
    'description': "Sharp teeth."
    }
]
