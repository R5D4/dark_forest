"""
Character classes.

Contains the following classes:
    Character
    Player
    Boar
"""

from random import randint
from random import choice
import combat

class Character(object):
    """
    Generic class for all game characters.

    New characters should subclass this class and extend the __init__ method.
    New character classes should define the following properties:
        self.attributes = {
            'str': int,
            'dex': int,
            'reflex': int,
            'AC': int,
            'max_HP': int,
            'max_mana': int
        }
        self.attacks = {
            'name1': Attack1(),
            'name2': Attack2()
            ...
        }
        self.desc = {
            'name': string,
            'job': string,
            'desc': string
        }
    """

    def __init__(self):
        self.health = {
            'HP': 0,
            'mana': 0
        }
        self.roll_attributes()
        self.health['HP'] = self.attributes['max_HP'] 
        self.health['mana'] = self.attributes['max_mana'] 
        self.inventory = {}
    
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


########## PLAYER CHARACTER ##########

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
            'slash': Slash(),
            'stab': Stab(),
            'shoot': Shoot()
        }
        self.desc = {
            'name': 'Hallas',
            'job': 'ranger',
            'desc': '"Tall-Leaf" in the common speech. A ranger from \
the North.'
        } 
        super(Player, self).__init__()
        self.print_stats()


########## BOSS CHARACTER ##########

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
            'charge': Charge(),
            'kick': Kick(),  
            'bite': Bite()
        }
        self.desc = {
            'name': 'Unknown',
            'job': 'wild boar',
            'desc': 'An enormous wild boar with thick black fur and long \
tusks.'
        } 
        super(Boar, self).__init__()
        self.print_stats()


########## PLAYER ATTACKS ##########

class Slash(combat.Attack):
    
    def __init__(self):
        self.details = {
            'prep_msg': "The %s slashes the %s with his elven long-knife!",
            'hit_crit_msg': "The elven long-knife opens up a gushing wound!",
            'hit_success_msg': "The elven long-knife cuts through!",
            'hit_fail_msg': "The elven long-knife bounces off!",
            'hit_attr': 'str',
            'hit_roll': '1d20',
            'hit_against': 'AC',
            'dmg_roll': '1d8',
            'dmg_base': 3
        }


class Shoot(combat.Attack):
    
    def __init__(self):
        self.details = {
            'prep_msg': "The %s lets fly an arrow from his longbow at the %s!",
            'hit_crit_msg': "The arrow pierces a vital organ!",
            'hit_success_msg': "The arrow pierces through!",
            'hit_fail_msg': "The arrow glances off!",
            'hit_attr': 'dex',
            'hit_roll': '1d20',
            'hit_against': 'AC',
            'dmg_roll': '1d8',
            'dmg_base': 3
        }


class Stab(combat.Attack):
    
    def __init__(self):
        self.details = {
            'prep_msg': "The %s stabs the %s with his hunting knife!",
            'hit_crit_msg': "The blade finds a softspot and sinks in!",
            'hit_success_msg': "The blade punctures through!",
            'hit_fail_msg': "The blade bounces off!",
            'hit_attr': 'str',
            'hit_roll': '1d10',
            'hit_against': 'AC',
            'dmg_roll': '1d8',
            'dmg_base': 1
        }


########## BOSS ATTACKS ##########

class Charge(combat.Attack):
    
    def __init__(self):
        self.details = {
            'prep_msg': "The %s charges the %s, leading with its tusks!",
            'hit_crit_msg': "The charge connects! The tusks are buried deep!",
            'hit_success_msg': "The tusks pierce the defences!",
            'hit_fail_msg': "The charge misses!",
            'hit_attr': 'dex',
            'hit_roll': '1d10',
            'hit_against': 'reflex',
            'dmg_roll': '1d10',
            'dmg_base': 7 
        }


class Kick(combat.Attack):
    
    def __init__(self):
        self.details = {
            'prep_msg': "The %s kicks the %s with its hooves!",
            'hit_crit_msg': "The kick lands square on!",
            'hit_success_msg': "The kick connects!",
            'hit_fail_msg': "The kick misses!",
            'hit_attr': 'str',
            'hit_roll': '1d10',
            'hit_against': 'reflex',
            'dmg_roll': '1d8',
            'dmg_base': 3
        }


class Bite(combat.Attack):
    
    def __init__(self):
        self.details = {
            'prep_msg': "The %s bites at the %s!",
            'hit_crit_msg': "An artery is opened by the razor-sharp teeth!",
            'hit_success_msg': "The teeth sink in!",
            'hit_fail_msg': "The teeth do not penetrate!",
            'hit_attr': 'str',
            'hit_roll': '1d20',
            'hit_against': 'AC',
            'dmg_roll': '1d8',
            'dmg_base': 2
        }

