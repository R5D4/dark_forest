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

# see data/attack_data.py for list of possible attack types

# huge array of dict objects specifying weapon characteristics
WEAPONS = [
    # New weapon template
    # {
    #   'name': <Weapon Name>
    #   'class': <Weapon Class>
    #   'attack': <weapon's attack type>
    #   'attribute': <the player attribute the weapon depends on>
    #   'min_str': <min str rating to use>
    #   'min_dex': <min dex rating to use>
    #   'hit_bonus': <weapon's hit bonus>
    #   'dmg_roll': <weapon's dmg die>
    #   'dmg_bonus': <weapon's dmg bonus>
    #   'AC_bonus': (<ability name>, <AC_bonus>)
    #   'description': <Flavor text description>
    # }
    {
    'name': 'Knight Sword',
    'class': 'bastard_sword',
    'atk_type': 'slash',
    'attribute': 'str',
    'require': {'str': 4, 'dex': 4},
    'bonus': {'str': 2, 'dex': 2, 'AC': 3},
    'dmg_roll': '1d8',
    'description': "A hand-and-a-half sword commonly used by men of Gondor.\
There are faint markings on the pommel depicting the tiered rings of Minas \
Tirith."
    },
    {
    'name': 'Elven Longbow',
    'class': 'bow',
    'atk_type': 'pierce',
    'attribute': 'dex',
    'require': {'str': 2, 'dex': 5},
    'bonus': {'str': 0, 'dex': 5, 'AC': 2},
    'dmg_roll': '1d8',
    'description': "An elegant lowbow made by one of the sylvan folk."
    },
    {
    'name': 'Hunting Knife',
    'class': 'knife',
    'atk_type': 'pierce',
    'attribute': 'dex',
    'require': {'str': 0, 'dex': 0},
    'bonus': {'str': 1, 'dex': 3, 'AC': 5},
    'dmg_roll': '1d6',
    'description': "A standard hunting knife. Simple but effective."
    },
#    {
#    'name': 'Estoc',
#    'class': '2h_sword',
#    'attack': ['pierce'],
#    'attribute': 'str',
#    'min_str': 5,
#    'min_dex': 3,
#    'hit_bonus': 3,
#    'dmg_roll': '1d8',
#    'dmg_bonus': 3,
#    'AC_bonus': ('parry', 1),
#    'description': "A really long and straight sword. It's stiff and has no \
#cutting edge. The blade comes to a fine point."
#    },
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

BOSS_WEAPONS = [
    {
    'name': 'Tusks',
    'class': 'head',
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
    'atk_type': 'pierce',
    'attribute': 'str',
    'require': {'str': 0, 'dex': 0},
    'bonus': {'str': 1, 'dex': 0, 'AC': 0},
    'dmg_roll': '1d6',
    'description': "Sharp teeth."
    }
]
