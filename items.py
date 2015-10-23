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
        self.item_type = TYPE_WEAPON
        self.desc.update(desc)
        self.generate_attacks()

    def generate_attacks(self):
        """ Generate Attack objects based on weapon description."""



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

