"""
Contains the Item class and its subclasses (Weapon, Armor) 
Contains functions to randomly generate an item.
"""

########## CONSTANTS ##########

TYPE_WEAPON = 'weapon'
TYPE_ARMOR = 'armor'
TYPE_CONSUME = 'consummable'

########## CLASS DEFINITIONS ##########


class Item(object):
    """ Base class for all items."""

    def __init__(self):
        self.item_type = None
        self.description = "Unidentified item."


class Weapon(Item):
    """ Represents a weapon."""

    def __init__(self, attacks, w_class, w_name):
        """ 
        attacks: list of combat.Attack objects
        w_class: weapon class e.g. 2h_sword
        w_name: weapon name e.g. claymore
        """
        self.item_type = TYPE_WEAPON
        self.w_class = w_class
        self.w_name = w_name
        self.description = "Unidentified weapon."
        self.attacks = attacks


class Armor(Item):
    """ Represents a piece of armor."""
    
########## ITEM GENERATORS ##########


def new_weapon():
    """ Return a randomly generated Weapon object."""
    # random weapon class
    w_class = choice(WEAPON_CLASS)
