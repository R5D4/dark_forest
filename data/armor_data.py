""" 
This module contains armor descriptions.
"""
# armor classes
#'cap'
#'helm'
#'mail'
#'plate'
#'shield'
#'leggings'
#'greaves'
#'shoes'
#'boots'

# huge array of dict objects specifying armor characteristics
ARMOR = [
    # New armor template
    # {
    #   'name': <Weapon Name>
    #   'class': <Weapon Class>
    #   'rarity': <0-99 higher is rarer>
    #   'slot': <list of slot id strings>
    #   'require': <minimum base stats required to equip>
    #   'bonus': <armor's stat bonuses>
    #   'description': <Flavour text description>
    # }
    {
    'name': 'Knight Shield',
    'class': 'shield',
    'rarity': 90,
    'slot': ['L_hand'],
    'require': {'str': 6, 'dex': 0},
    'bonus': {'str': 0, 'dex': -4, 'AC': 10},
    'description': "A large sturdy shield almost as tall as you. The White \
Tree of Minath Tirith is painted on top of a black background."
    },
    {
    'name': 'Knight Helmet',
    'class': 'helm',
    'rarity': 60,
    'slot': ['head'],
    'require': {'str': 4, 'dex': 0},
    'bonus': {'str': 0, 'dex': -1, 'AC': 3},
    'description': "A full-face helmet with a visor."
    },
]
