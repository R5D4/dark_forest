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

# list of possible attack types
#   thrust
#   slash
#   smash
#   shoot

# huge array of dict objects specifying weapon characteristics
WEAPONS = [
    # New attack template
    # {
    #   'name': <Weapon Name>,
    #   'class': <Weapon Class>,
    #   'attacks': <Allowed attack types for the weapon>,
    #   'base': <Base stat bonus for each attack, for dmg and hit>
    #   'description': <Flavor text description>
    # }
    {
    'name': 'Estoc',
    'class': '2h_sword',
    'attacks': ['thrust'],
    'base': {
            'thrust': {'dmg': 3, 'hit': 2}
            },
    'description': "A really long and straight sword. It's stiff and has no \
cutting edge. The blade comes to a fine point."
    },

    {
    'name': 'Long Sword',
    'class': '2h_sword',
    'attacks': ['slash', 'thrust'],
    'base': {
            # dmg +2, hit +1 for slashing with this weapon
            'slash': {'dmg': 2, 'hit': 1},
            # dmg +2, hit +2 for thrusting with this weapon
            'thrust': {'dmg': 2, 'hit': 2}
            },
    'description': "It's a long... sword. The blade is straight and double-\
edged."
    },

    {
    'name': 'Knight Sword',
    'class': 'bastard_sword',
    'attacks': ['slash', 'thrust'],
    'base': {
            'slash': {'dmg': 2, 'hit': 2},
            'thrust': {'dmg': 1, 'hit': 1}
            },
    'description': "A hand-and-a-half sword commonly used by men of Gondor.\
There are faint markings on the pommel depicting the tiered rings of Minas \
Tirith."
    },

    {
    'name': 'Elven Longbow',
    'class': 'bow',
    'attacks': ['shoot'],
    'base': {
            'shoot': {'hit': 3}
            },
    'description': "An elegant lowbow made by one of the sylvan folk."
    }
]
