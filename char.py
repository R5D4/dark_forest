"""
Character classes.

Contains the following classes:
    Character
    Player
    Boar
"""

from random import randint
from random import choice
from util import roll
import combat
import items


class Character(object):
    """
    Generic class for all game characters. Subclass and override equipment
        rules. 

    All characters have the following attributes:
        base_stats: 
            character's base stats
        bonus_stats:: 
            bonus from equipment or enchantments
        effective_stats: 
            base + bonus

    stats (base, bonus, effective):
        {'str': int, 'dex': int, 'AC': int, 'max_HP': int}
    health:
        {'HP': int}
    desc:
        {'name': string, 'job': string, 'bio': string}
    inventory:
        [Item1, Item2, ...}
    equipped:
        {slot: Item, ...}
    attacks:
        {attack name: Attack obj}
    """

    def __init__(self, min_stats, desc, equip_slots):
        """ Create a character with given minimum stats."""
        # initialize to empty
        self.base_stats = {}
        self.bonus_stats = {}
        self.effective_stats = {}
        self.health = {}
        self.desc = {}
        self.inventory = []
        self.equipped = {}
        self.attacks = {}
        # fill in with provided info
        self.init_stats(min_stats)
        self.health = { 'HP': self.effective_stats['max_HP'] }
    
    def init_base_stats(self, min_stats):
        """ Initialize character stats."""
        # zero out all stats
        init = {'str': 0, 'dex': 0, 'AC': 0, 'max_HP': 0}
        self.base_stats.update(init)
        self.bonus_stats.update(init)
        self.effective_stats.update(init)
        # base stats = min stats + 2d6
        self.base_stats.update(min_stats)
        for stat in self.base__stats.keys():
            self.base_stats[stat] += roll('2d6', False)[0]
        # update effective stats
        self.update_stats()

    def update_stats(self):
        """ Calculate bonus and effective stats."""
        # calculate bonus from equipment
        # update effective stats
        for s in self.base_stats.keys():
            self.effective_stats[s] = self.base_stats[s] + self.bonus_stats[s]
        
    def get_stats(self):
        """ Return character stats in a formatted string."""
        stats = []
        stats.append("DESCRIPTION")
        for s in self.desc.keys():
            stats.append("%s: %s" % (s, self.desc[s]))
        stats.append("ATTRIBUTES")
        for s in self.attributes.keys():
            stats.append("%s: %s" % (s, self.attributes[s]))
        stats.append("ATTACKS")
        for s in self.attacks.keys():
            stats.append(s)
        return '\n'.join(stats)

    def pick_up(self, item):
        """ Add item to inventory. item is an Item object."""
        self.inventory.append(item)

    def get_inventory(self):
        """ Return inventory desc. Uses index as unique ID for each item."""
        inv = []
        #print self.inventory
        for index, item in enumerate(self.inventory):
            if item.equipped:
                eq = '[E]'
            else:
                eq = ''
            inv.append( "{}: {}{}".format(index, item.desc['name'], eq) )
        return '\n'.join(inv)

    def get_equipped(self):
        """ Return equipped items' names."""
        eq = []
        for loc, item in self.equipped.items():
            if item is None:
                desc = 'Empty'
            else:
                desc = item.desc['name']
            eq.append('{}: {}'.format(loc, desc))
        return '\n'.join(eq)
            
    def take_damage(self, dmg):
        """ Take damage. Updates the 'HP' attribute."""
        self.health['HP'] -= dmg
        print "The %s took %d damage!" % (self.desc['job'], dmg)

########## PLAYER CHARACTER ##########


class Player(Character):
    """ Player class."""

    def __init__(self):
        """ Extends Character.__init__"""
        self.set_base_attr()
        super(Player, self).__init__()
        self.init_items()
        self.roll_items()

    def set_base_attr(self):
        """ Set base attributes."""
        # base attributes
        self.attributes = {
            'str': 0,
            'dex': 0,
            'AC': 10,
            'max_HP': 20
        }
        self.desc = {
            'name': 'Hallas',
            'job': 'ranger',
            'desc': '"Tall-Leaf" in the common speech. A ranger from \
the North.'
        } 

    def init_items(self):
        """ Initialize inventory and equipment slots."""
        self.inventory = []
        self.equipped = {
            'head': None,
            'torso': None,
            'L_hand': None,
            'R_hand': None,
            'legs': None,
            'feet': None
        }

    def roll_items(self):
        """ Generate random items, weapons and armor."""
        self.pick_up(items.new_weapon())

    def equip(self, item):
        """ Equip the item. Return True if success. False otherwise."""
        # Decide where to equip the item
        # for now equip everything in right hand
        self.equipped['R_hand'] = item
        # update item's equipped status
        item.equipped = True
        return True

    def unequip(self, slot):
        """ Unequip item in given slot. Return message of what happened."""
        # if there is something equipped in the slot
        if self.equipped[slot] is not None:
            item = self.equipped[slot]
            # remove the item from equipped
            self.equipped[slot] = None
            # update item status to indicate it's unequipped
            item.equipped = False
            # set message indicating success
            message = "Unequipped {}.".format(item.desc['name'])
        # else - nothing equipped in the slot
        else:
            # set message indicating failure
            message = "Nothing equipped."
        # return message
        return message


########## BOSS CHARACTER ##########


class Boar(Character):
    """ Boar class (boss)."""

    def __init__(self):
        """ Extends Character.__init__"""
        # base attributes
        self.attributes = {
            'str': 7,
            'dex': 2,
            'AC': 10,
            'max_HP': 20,
        }
        super(Boar, self).__init__()
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
        self.inventory = []
        self.equipped = {}

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

