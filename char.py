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

    def __init__(self, min_stats, equip_slots, desc):
        """ 
        Create a character with given minimum stats.
        
        min_stats: {'str': int, 'dex': int, 'AC': int, 'max_HP': int}
        equip_slots: ['head', 'torso', 'legs', ...]
        desc: {'name': string, 'job': string, 'bio': string}
        """
        # initialize to empty
        self.desc = {}
        self.base_stats = {}
        self.bonus_stats = {}
        self.effective_stats = {}
        self.health = {}
        self.inventory = []
        self.equipped = {}
        self.attacks = {}
        # update stats and health
        self.init_stats(min_stats)
        self.health = { 'HP': self.effective_stats['max_HP'] }
        # update equipment slots
        self.init_equip_slots(equip_slots)
        # update description
        self.desc.update(desc)
    
    def init_stats(self, min_stats):
        """ Initialize character stats."""
        # zero out all stats
        init = {'str': 0, 'dex': 0, 'AC': 0, 'max_HP': 0}
        self.base_stats.update(init)
        self.bonus_stats.update(init)
        self.effective_stats.update(init)
        # base stats = min stats + 2d6
        self.base_stats.update(min_stats)
        for stat in self.base_stats.keys():
            self.base_stats[stat] += roll('2d6', False)[0]
        # update effective stats
        self.update_stats()

    def init_equip_slots(self, slots):
        """ Add equipment slots."""
        for s in slots:
            self.equipped[s] = None

    def update_stats(self):
        """ Calculate bonus and effective stats."""
        # calculate bonus from equipment
        # update effective stats
        for s in self.base_stats.keys():
            self.effective_stats[s] = self.base_stats[s] + self.bonus_stats[s]
        
    def get_stats(self):
        """ Return character stats in a formatted string."""
        stats = []
        # description
        stats.append("DESCRIPTION:")
        for k, v in self.desc.items():
            stats.append("{}: {}".format(k, v))
        # base stats
        stats.append("BASE STATS:")
        for k, v in self.base_stats.items():
            stats.append("{}: {}".format(k, v))
        # bonus stats
        stats.append("BONUS STATS:")
        for k, v in self.bonus_stats.items():
            stats.append("{}: {}".format(k, v))
        # effective stats
        stats.append("EFFECTIVE STATS:")
        for k, v in self.effective_stats.items():
            stats.append("{}: {}".format(k, v))
        # health
        stats.append("HEALTH:")
        for k, v in self.health.items():
            stats.append("{}: {}".format(k, v))
        # attacks
        stats.append("ATTACKS")
        for k in self.attacks.keys():
            stats.append(k)
        return '\n'.join(stats)

    def pick_up(self, item):
        """ Add item to inventory. item is an Item object."""
        self.inventory.append(item)

    def drop(self, itemID):
        """ Drop the item from inventory with itemID."""
        # NOTE: Implement this
        pass

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
        """ 
        Extends Character.__init__

        Create a fully initialized player object.
        """
        # set player details
        min_stats = { 'str': 0, 'dex': 0, 'AC': 10, 'max_HP': 20 }
        equip_slots = ['head', 'torso', 'L_hand', 'R_hand', 'legs', 'feet'] 
        desc = {
            'name': 'Hallas',
            'job': 'ranger',
            'desc': '"Tall-Leaf" in the common speech. A ranger from \
the North.'
        } 
        # use the Character class __init__ method
        super(Player, self).__init__(min_stats, equip_slots, desc)
        # add default item
        self.roll_items()

    def roll_items(self):
        """ Generate random items, weapons and armor."""
        self.pick_up(items.new_weapon())

    def equip(self, item):
        """ Equip the item. Return True if success. False otherwise."""
        # Decide where to equip the item
        # NOTE: for now equip everything in right hand
        self.equipped['R_hand'] = item
        # update item's equipped status
        item.equipped = True
        if item.item_type == 'weapon':
            self.attacks.update({item.desc['atk_type']: item.attack})
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
        # set boss details
        min_stats = { 'str': 7, 'dex': 2, 'AC': 10, 'max_HP': 20 }
        equip_slots = ['head', 'torso', 'FL_hoof', 'FR_hoof', 
                       'HL_hoof', 'HR_hoof'] 
        desc = {
            'name': 'Unknown',
            'job': 'wild boar',
            'desc': 'An enormous wild boar with thick black fur and long \
tusks.'
        } 
        super(Boar, self).__init__(min_stats, equip_slots, desc)
        # add equipment and attacks
        self.roll_items()
        self.default_equip()
        self.attacks = {
            'charge': Charge(),
            'kick': Kick(),  
            'bite': Bite()
        }

    def roll_items(self):
        """ Put default items in inventory."""
        pass

    def default_equip(self):
        """ Equip default items."""
        pass

########## PLAYER ATTACKS ##########


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
            'prep_msg': "The %s charges the %s!",
            'hit_crit_msg': "The charge hits square on!",
            'hit_success_msg': "The charge connects!",
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

