"""
Contains the Weapon class. 

Maybe later we'll have a generic Item class and Armor as well.
"""

TYPE_WEAPON = 'weapon'
TYPE_ARMOR = 'armor'
TYPE_ITEM = 'item'


class Item(object):
    """ Base class for all items, including weapons and armor."""

    def __init__(self):
        self.item_type = None
        self.description = "Unidentified item."


class Weapon(Item):
    """ Parent class for all weapon objects."""

    def __init__(self, attacks):
        """ 
        attacks: list of combat.Attack objects
        """
        self.item_type = TYPE_WEAPON
        self.description = "Some kind of weapon."
        self.attacks = attacks

