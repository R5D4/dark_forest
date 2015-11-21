"""
Character classes.

Contains the following classes:
    Character
    Player
    Boar
"""

from math import floor
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
        [Item1, Item2, ...]
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
        # base stats = min stats + 2d6.
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
        # clear bonus stats
        init = {'str': 0, 'dex': 0, 'AC': 0, 'max_HP': 0}
        self.bonus_stats.update(init)
        # clear attacks
        self.attacks = {}

        # update stats for each equipped item
        for item in self.equipped.values():
            if item: # not None
                # calculate bonus from equipment
                for attr, bonus in item.desc['bonus'].items():
                    self.bonus_stats[attr] += bonus
                # update attacks
                if item.item_type == 'weapon':
                    self.attacks.update({item.desc['atk_type']: item.attack})

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
        if not self.inventory: # empty
            return "Inventory is empty."
        msg = []
        for index, item in enumerate(self.inventory):
            if item.equipped:
                eq = '[E]'
            else:
                eq = ''
            msg.append( "{}: {}{}".format(index, item.desc['name'], eq) )
        return '\n'.join(msg)

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
            
    def update_hp(self, d):
        """ 
        Updates the 'HP' attribute and return output string.
        
        d < 0: damage
        d > 0: heal
        d = 0: nothing happened
        """
        new_hp = self.health['HP'] + d
        # prevent hp from going over max hp, it can still go lower than 0
        if new_hp > self.effective_stats['max_HP']:
            new_hp = self.effective_stats['max_HP']
        # changed = actual HP change
        changed = new_hp - self.health['HP']
        self.health['HP'] = new_hp
        # create output string depending on HP change
        if changed < 0: # damaged
            msg = "The {} took {} damage!".format(self.desc['job'], -changed)
        elif changed > 0: # healed
            msg = "The {} healed {} HP.".format(self.desc['job'], changed)
        else: # no HP change
            msg = "Nothing happened."
        return msg

########## PLAYER CHARACTER ##########


class Player(Character):
    """ Player class."""

    def __init__(self):
        """ 
        Extends Character.__init__

        Create a fully initialized player object.
        """
        # set player details
        min_stats = { 'str': 0, 'dex': 0, 'AC': 10, 'max_HP': 100 }
        equip_slots = ['head', 'torso', 'L_hand', 'R_hand', 'legs', 'feet'] 
        desc = {
            'name': 'Hallas',
            'job': 'ranger',
            'desc': '"Tall-Leaf" in the common speech. A ranger from \
the North.'
        } 
        # use the Character class __init__ method
        super(Player, self).__init__(min_stats, equip_slots, desc)
        # add and equip default item
        self.roll_items()
        self.equip_default()

    def roll_items(self):
        """ Generate default equipment."""
        self.pick_up(items.get_weapon('Hunting Knife'))

    def equip_default(self):
        """ Equip all default items."""
        for item in self.inventory:
            self.equip(item)

    def equip(self, item):
        """ Equip the item. Return True if success. False otherwise."""
        # Check if item already equipped
        if item.equipped:
            return "The item is already equipped."
        # Check stat requirements (base stats)
        for attr, req in item.desc['require'].items():
            if self.base_stats[attr] < req:
                return "Unable to equip {}, need {}.".format(item.desc['name'],
                                                         item.desc['require'])
        # Figure out which slots to use
        #if item.desc['class'] in ['2h_sword', 'bow']:
        #    self.unequip('R_hand')
        #    self.unequip('L_hand')
        #    self.equipped['R_hand'] = item
        #    self.equipped['L_hand'] = item
        #else:
        # NOTE: Add 2h support
        self.unequip('R_hand')
        self.equipped['R_hand'] = item
        item.equipped = True
        message = "Equipped {}.".format(item.desc['name'])
        self.update_stats()
        return message

    def unequip(self, slot):
        """ Unequip item in given slot. Return message of what happened."""
        # if there is something equipped in the slot
        if self.equipped[slot]: # not None
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
        # update stats
        self.update_stats()
        # return message
        return message

    def rest(self):
        """ Rest for one clock tick. Recover some HP."""
        # recover 5% of max HP per tick
        hp = int(floor((0.05 * self.effective_stats['max_HP'])))
        return self.update_hp(hp)

    def sleep(self):
        """ Sleep for one clock tick. Recover some HP."""
        # recover 8% of max HP per tick
        hp = int(floor((0.08 * self.effective_stats['max_HP'])))
        return self.update_hp(hp)

########## BOSS CHARACTER ##########


class Boar(Character):
    """ Boar class (boss)."""

    def __init__(self):
        """ Extends Character.__init__"""
        # set boss details
        min_stats = { 'str': 7, 'dex': 2, 'AC': 10, 'max_HP': 150 }
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
        self.equip_default()

    def roll_items(self):
        """ Put default items in inventory."""
        self.pick_up(items.boss_weapon())

    def equip_default(self):
        """ Equip default items."""
        for item in self.inventory:
            self.equip(item)

    def equip(self, item):
        """ Equip the item. Return True if success. False otherwise."""
        # Decide where to equip the item
        # NOTE: for now equip everything on the head
        self.equipped['head'] = item
        # update item's equipped status
        item.equipped = True
        if item.item_type == 'weapon':
            self.attacks.update({item.desc['atk_type']: item.attack})
        # update stats
        self.update_stats()
        return "Equipped {}.".format(item.desc['name'])

