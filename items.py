"""
Contains the Item class and its subclasses (Weapon, Armor) 
Contains functions to randomly generate an item.
"""

import data.weapon_data as wd
from random import choice
import combat

# items types
# 'weapon'
# 'armor'
# 'consummable'

########## CLASS DEFINITIONS ##########


class Item(object):
    """ Base class for all items."""

    def __init__(self):
        self.item_type = None
        self.equipped = False
        self.desc = {'name': "Unidentified item."} # all items must have name

    def get_info(self):
        """ Return string containing formatted weapon description."""
        info = []
        for s in self.desc.keys():
            info.append("{}: {}".format(s, self.desc[s]))
        return '\n'.join(info)


class Weapon(Item):
    """ Represents a weapon."""

    def __init__(self, desc):
        super(Weapon, self).__init__()
        # initialize attributes
        self.item_type = 'weapon'
        self.desc.update(desc)
        self.attack = None
        # generate the associated Attack object
        self.generate_attack(desc)

    def generate_attack(self, desc):
        """ Generate Attack object based on weapon description."""
        attack = combat.Attack(desc)
        self.attack = attack


class Armor(Item):
    """ Represents a piece of armor."""
    

class Consummable(Item):
    """ Represents a consummable item."""


########## ITEM GENERATORS ##########


def get_weapon(name):
    """
    Return a Weapon object by name.
    """
    for w_desc in wd.WEAPONS:
        if w_desc['name'] == name:
            break
    return Weapon(w_desc)


def new_weapon():
    """ 
    Return a player Weapon object created from a weapon description.
    
    Weapon descriptions are in the data.weapon_data module.
    """
    # randomly grab a weapon description
    w_desc = choice(wd.WEAPONS)
    return Weapon(w_desc)


def boss_weapon():
    """
    Return a boss Weapon object created from a weapon description.

    Weapon descriptions are in data.weapon_data
    """
    w_desc = choice(wd.BOSS_WEAPONS)
    return Weapon(w_desc)
