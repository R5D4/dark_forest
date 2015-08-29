"""
Combat-related resources.

Contains the function begin_combat and the Attack class.
"""

from random import choice
from util import roll

# user types this to signal attack
ATTACK = 'attack'


def begin_combat(characters):
    """
    Start combat.

    Start combat between the 'player' and 'boar' characters.
    Return 'death' if player dies or 'win' if boar dies.
    There is currently no way to exit combat in any other way once entered.
    """
    player = characters['player']
    boar = characters['boar']

    print "*" * 10,
    print " Entering combat! ",
    print "*" * 10
    
    # Determine initiative

    print "Rolling initiatives:"
    player_init = roll('1d20', True)[0]
    boar_init = roll('1d20', True)[0]
    print "Player's initiative: %d" % player_init
    print "Boar's initiative: %d" % boar_init
    if player_init > boar_init:
        turn = 'player'
    else:
        turn = 'boar'

    print "{} goes first.".format(turn),
    raw_input("Press any key to continue")

    # Start combat loop

    while True:
        print '-' * 20
        if turn == 'player':
            print "Player's turn:"
            print "HP: %d" % player.health['HP']
            action = raw_input("> ")
            if action in player.attacks.keys():
                player_attack = player.attacks[action]
                player_attack.attack(player, boar)
            else:
                print "You can't do that."
            turn = 'boar'
            raw_input("Press any key to continue.")
        elif turn == 'boar':
            print "Boar's turn:"
            #print "HP: %d" % boar.health['HP']
            # output bloodied message if HP < 30%
            if boar.health['HP']/float(boar.attributes['max_HP']) < 0.3:
                print "The boar is bloodied!"
            boar_attack = boar.attacks[choice(boar.attacks.keys())]
            boar_attack.attack(boar, player)
            turn = 'player'
        
        if player.health['HP'] <= 0:
            return 'death' 
        elif boar.health['HP'] <= 0:
            return 'win' 


class Attack(object):
    """
    Base class for an attack.

    New attacks should subclass this class and override the __init__ method.
    New attack subclasses need to define self.details.
    """

    def __init__(self):
        """
        __init__ method in Attack class does nothing.

        Subclasses need to define self.details as follows in their __init__.
        self.details = {
            'prep_msg': string - msg printed when attack begins
            'hit_crit_msg': string - msg printed when critical is rolled
            'hit_success_msg': string - msg printed when successful attack
            'hit_fail_msg': string - msg when attack fails
            'hit_attr': character attribute to add to hit chance e.g. 'str'
            'hit_roll': dice roll format e.g. '1d10'
            'hit_against': enemy attribute to hit against e.g. 'AC'
            'dmg_roll': dice roll format e.g. '2d6'
            'dmg_base': integer - min damage if successful hit
        }
        """

    def attack(self, from_char, to_char):
        """ Perform an attack represented by self from from_char to to_char."""

        print self.details['prep_msg'] % (from_char.desc['job'], 
                                      to_char.desc['job'])
        # calculate hit
        # Hit formula:
        #   attacker's hit_attr attribute + hit_roll VS
        #   defender's hit_against attribute
        print "Calculating hit chance:",
        hit_attr = from_char.attributes[self.details['hit_attr']]
        hit_roll, crit_roll = roll(self.details['hit_roll'], True)
        hit_against = to_char.attributes[self.details['hit_against']]
        hit = hit_attr + hit_roll
        print "%d against %d" % (hit, hit_against)
        
        # calculate damage
        # Dmg formula:
        #   Critical roll and hit = max damage
        #   Critical roll and miss = roll for normal damage
        #   Noncrit roll and miss = 0 damage
        #   Normal damage = attack's dmg_base + dmg_roll
        if hit_roll == crit_roll:
            # crit and successful hit, max damage
            if hit > hit_against:
                print "Critical Hit! Max Damage!"
                print self.details['hit_crit_msg']
                dmg = self.details['dmg_base'] + \
                      roll(self.details['dmg_roll'], False)[1] 
                to_char.take_damage(dmg)
            else:
                # crit but not enough to hit, regular damage
                print "Critical Hit!"
                print self.details['hit_success_msg']
                dmg = self.details['dmg_base'] + \
                      roll(self.details['dmg_roll'], True)[0] 
                to_char.take_damage(dmg)
        elif hit > hit_against:
            print self.details['hit_success_msg']
            print "Calculating damage:",
            dmg = self.details['dmg_base'] + \
                  roll(self.details['dmg_roll'], True)[0] 
            to_char.take_damage(dmg)
        else:
            print self.details['hit_fail_msg']

