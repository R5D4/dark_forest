""" 
This module contains weapon descriptions.
"""

# list of weapon classes
#   2h_sword
#   bastard_sword
#   1h_sword
#   knife
#   axe
#   bow

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
    #   'dmg_die': <weapon's dmg die>
    #   'dmg_bonus': <weapon's dmg bonus>
    #   'AC_bonus': (<ability name>, <AC_bonus>)
    #   'description': <Flavor text description>
    # }
    {
    'name': 'Knight Sword',
    'class': 'bastard_sword',
    'attack': ['slash'],
    'attribute': 'str',
    'min_str': 4,
    'min_dex': 4,
    'hit_bonus': 2,
    'dmg_die': '1d8',
    'dmg_bonus': 2,
    'AC_bonus': ('parry', 3),
    'description': "A hand-and-a-half sword commonly used by men of Gondor.\
There are faint markings on the pommel depicting the tiered rings of Minas \
Tirith."
    },
    {
    'name': 'Estoc',
    'class': '2h_sword',
    'attack': ['thrust'],
    'attribute': 'str',
    'min_str': 5,
    'min_dex': 3,
    'hit_bonus': 3,
    'dmg_die': '1d8',
    'dmg_bonus': 3,
    'AC_bonus': ('parry', 1),
    'description': "A really long and straight sword. It's stiff and has no \
cutting edge. The blade comes to a fine point."
    },
    {
    'name': 'Long Sword',
    'class': '2h_sword',
    'attack': ['slash'],
    'attribute': 'str',
    'min_str': 5,
    'min_dex': 3,
    'hit_bonus': 2,
    'dmg_die': '1d8',
    'dmg_bonus': 3,
    'AC_bonus': ('parry', 3),
    'description': "It's a long... sword. The blade is straight and double-\
edged."
    },
    {
    'name': 'Elven Longbow',
    'class': 'bow',
    'attack': ['shoot'],
    'attribute': 'dex',
    'min_str': 0,
    'min_dex': 5,
    'hit_bonus': 4,
    'dmg_die': '1d6',
    'dmg_bonus': 2,
    'AC_bonus': ('dodge', 3),
    'description': "An elegant lowbow made by one of the sylvan folk."
    },
]
