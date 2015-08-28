"""
Character classes.

Contains the following classes:
    Character
    Player
    Boar
"""

from random import randint
from random import choice
import map_
import combat

class Character(object):
    """
    Generic class for all game characters.

    New characters should subclass this class and extend the __init__ method.
    The following attributes should be changed to suit the new character:
        self.attributes
        self.attacks
        self.desc
    """

    def __init__(self):
        # base attributes
#        self.attributes = {
#            'str': 0,
#            'dex': 0,
#            'reflex': 0,
#            'AC': 0,
#            'max_HP': 0,
#            'max_mana': 0
#        }
#        self.attacks = {}
#        self.desc = {
#            'name': None,
#            'job': None,
#            'desc': None
#        } 
        self.health = {
            'HP': 0,
            'mana': 0
        }
        self.roll_attributes()
        self.health['HP'] = self.attributes['max_HP'] 
        self.health['mana'] = self.attributes['max_mana'] 
    
    def roll_attributes(self):
        """ Roll some dice to add to base attribute values."""
        for stat in self.attributes.keys():
            self.attributes[stat] += randint(1, 6) + randint(1, 6)
        
    def print_stats(self):
        """ Print character stats."""
        print "DESCRIPTION"
        for s in self.desc.keys():
            print "%s: %s" % (s, self.desc[s])
        print "\nATTRIBUTES"
        for s in self.attributes.keys():
            print "%s: %s" % (s, self.attributes[s])
        print "\nATTACKS"
        for s in self.attacks.keys():
            print s

    def take_damage(self, dmg):
        """ Take damage. Updates the 'HP' attribute."""
        self.health['HP'] -= dmg
        print "The %s took %d damage!" % (self.desc['job'], dmg)


class Player(Character):
    """ Player class."""

    def __init__(self):
        """ Extends Character.__init__"""
        # base attributes
        self.attributes = {
            'str': 3,
            'dex': 8,
            'reflex': 10,
            'AC': 7,
            'max_HP': 10,
            'max_mana': 5
        }
        self.attacks = {
            'slash': combat.Slash(),
            'stab': combat.Stab(),
            'shoot': combat.Shoot()
        }
        self.desc = {
            'name': 'Hallas',
            'job': 'ranger',
            'desc': '"Tall-Leaf" in the common speech. An exiled ranger from \
the North.'
        } 
        super(Player, self).__init__()
        self.print_stats()


class Boar(Character):
    """ Boar class (boss)."""

    def __init__(self):
        """ Extends Character.__init__"""
        # base attributes
        self.attributes = {
            'str': 7,
            'dex': 2,
            'reflex': 5,
            'AC': 10,
            'max_HP': 20,
            'max_mana': 0
        }
        self.attacks = {
            'charge': combat.Charge(),
            'kick': combat.Kick(),  
            'bite': combat.Bite()
        }
        self.desc = {
            'name': 'Unknown',
            'job': 'wild boar',
            'desc': 'An enormous wild boar with thick black fur and long \
tusks.'
        } 
        super(Boar, self).__init__()
        self.print_stats()
