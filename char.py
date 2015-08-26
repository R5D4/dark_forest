# Contains the character profile

from random import randint
from random import choice
import map_
import combat

class Character(object):

    def __init__(self, bonus):
        pass
        #self.attributes = {
        #    'str': 0,
        #    'dex': 0,
        #    'reflex': 0,
        #    'AC': 0,
        #    'HP': 0
        #}
        #self.attacks = {}
        #self.desc = {} 
        #for stat in self.attributes.keys():
        #    self.attributes[stat] += bonus + randint(1, 6) + randint(1, 6)

    # print stats
    def print_stats(self):
        print "DESCRIPTION"
        for s in self.desc.keys():
            print "%s: %s" % (s, self.desc[s])
        print "\nATTRIBUTES"
        for s in self.attributes.keys():
            print "%s: %s" % (s, self.attributes[s])

    # take damage
    def take_damage(self, dmg):
        self.attributes['HP'] -= dmg
        print "The %s took %d damage!" % (self.desc['job'], dmg)


class Player(Character):

    def __init__(self, bonus):
        # base stats
        self.attributes = {
            'str': 3,
            'dex': 8,
            'reflex': 10,
            'AC': 7,
            'HP': 10,
            'max_HP': 0
        }
        self.attacks = {
            'slash': combat.Slash(),
            'stab': combat.Stab(),
            'shoot': combat.Shoot()
        }
        self.desc = {
            'name': 'Hallas',
            'job': 'ranger',
            'desc': 'Hallas Tall-Leaf, an exiled ranger from the North.'
        } 
        for stat in self.attributes.keys():
            self.attributes[stat] += bonus + randint(1, 6) + randint(1, 6)
        self.attributes['max_HP'] = self.attributes['HP']

        self.print_stats()


class Boar(Character):

    def __init__(self, bonus):
        # base stats
        self.attributes = {
            'str': 7,
            'dex': 2,
            'reflex': 5,
            'AC': 10,
            'HP': 20,
            'max_HP': 0
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
        for stat in self.attributes.keys():
            self.attributes[stat] += bonus + randint(1, 6) + randint(1, 6)
        self.attributes['max_HP'] = self.attributes['HP']

        self.print_stats()


