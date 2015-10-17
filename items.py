"""
Contains the Item class and its subclasses (Weapon, Armor) 
Contains functions to randomly generate an item.
"""

import data.weapon_data as wd
from random import choice

########## CONSTANTS ##########

TYPE_WEAPON = 'weapon'
TYPE_ARMOR = 'armor'
TYPE_CONSUME = 'consummable'

########## CLASS DEFINITIONS ##########


class Item(object):
    """ Base class for all items."""

    def __init__(self):
        self.item_type = None


class Weapon(Item):
    """ Represents a weapon."""

    def __init__(self, desc):
        self.item_type = TYPE_WEAPON
        self.desc = desc

    def get_info(self):
        """ Return string containing formatted weapon description."""
        info_str = ""
        for s in self.desc.keys():
            info_str += "{}: {}\n".format(s, self.desc[s])
        return info_str


class Armor(Item):
    """ Represents a piece of armor."""
    

class Consummable(Item):
    """ Represents a consummable item."""


########## ITEM GENERATORS ##########


def new_weapon():
    """ 
    Return a Weapon object created from a weapon description.
    
    Weapon descriptions are in the data.weapon_data module.
    """
    # randomly grab a weapon description
    w_desc = choice(wd.WEAPONS)
    return Weapon(w_desc)

