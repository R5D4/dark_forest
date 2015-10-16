""" 
This module contains data on various weapons.
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
WEAPONS = 
[
    {   
    'w_name': 'Estoc',
    'w_class': '2h_sword',
    'attacks': ['thrust'],
    'bonus': {
             'thrust': {'dmg': 3, 'hit': 2}
             },
    'description': "A really long and straight sword. It's stiff and has no \
cutting edge. The blade comes to a fine point."
    },

    {
    'w_name': 'Long Sword',
    'w_class': '2h_sword',
    'attacks': ['slash', 'thrust'],
    'bonus': {
             'slash': {'dmg': 2, 'hit': 1}
             'thrust': {'dmg': 2, 'hit': 2}
             },
    'description': "It's a long... sword. The blade is straight and double-\
edged."
    },

    {
    'w_name': 'Knight Sword',
    'w_class': 'bastard_sword',
    'attacks': ['slash', 'thrust'],
    'bonus': {
             'slash': {'dmg': 2, 'hit': 2}
             'thrust': {'dmg': 1, 'hit': 1}
             },
    'description': "A hand-and-a-half sword commonly used by men of Gondor.\
There are faint markings on the pommel depicting the tiered rings of Minas \
Tirith."
    }
]
