"""
Combat-related resources.

Contains the function begin_combat and the Attack class.
"""

from random import choice
from util import roll
import data.attack_data as atk_data

# user types this to signal attack
ATTACK = 'attack'
ENV_ACTIONS = {
              'run': ['r', 'run']
              }
# make single list of supported actions to check against user action
SUPPORTED_ACTIONS = \
    [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
# all hits roll 1d20
HIT_ROLL = '1d20'


########## MODULE FUNCTIONS ##########


def new_attack(weapon):
    """ Generate a new Attack object based on a Weapon object."""
    pass


def begin_combat(characters, scene, can_run):
    """
    Start combat.

    Start combat between the 'player' and 'boar' characters.
    Return 'death' if player dies or 'win' if boar dies.
    """
    # characters is a dict with an entry for key 'player' and 'boar'
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
            # loop until valid combat command is entered
            valid = False
            while not valid:
                action = raw_input("> ")
                if action in player.attacks.keys():
                    player_attack = player.attacks[action]
                    player_attack.attack(player, boar)
                    valid = True
                elif action in SUPPORTED_ACTIONS:
                    if action in ENV_ACTIONS['run'] and can_run:
                        print "Run away! Run away!"
                        return run_away(scene)               
                    elif action in ENV_ACTIONS['run'] and not can_run:
                        print "Can't run away!"
                    valid = True
                else:
                    print "You can't do that."
            turn = 'boar'
            raw_input("Press any key to continue.")
        elif turn == 'boar':
            print "Boar's turn:"
            #print "HP: %d" % boar.health['HP']
            # output bloodied message if HP < 30%
            if boar.health['HP']/float(boar.effective_stats['max_HP']) < 0.3:
                print "The boar is bloodied!"
            boar_attack = boar.attacks[choice(boar.attacks.keys())]
            boar_attack.attack(boar, player)
            turn = 'player'
        
        if player.health['HP'] <= 0:
            return 'death' 
        elif boar.health['HP'] <= 0:
            return 'win' 


def run_away(scene):
    """ Run away from combat. Return name of a random adjacent location."""
    scene.clock_tick()
    name = choice(scene.exits.values())
    return name

########## ATTACK CLASS ##########

class Attack(object):
    """
    Represents an attack.
    """

    def __init__(self, wpn_desc):
        """
        Create an Attack object depending on attack type and weapon

        wpn_desc is the dict containing weapon data
        """
        # get weapon information
        self.wpn_name = wpn_desc['name']
        self.attribute = wpn_desc['attribute']
        self.dmg_roll = wpn_desc['dmg_roll']
        # get combat messages
        atk_type = wpn_desc['atk_type']
        self.init_messages(atk_type)

    def init_messages(self, atk_type):
        """
        Initialize attack messages based on attack type.
        """
        self.messages = {}
        # Get combat messages from attack data for the attack type
        # NOTE: add checks here
        self.messages.update(atk_data.ATTACKS[atk_type])
        self.messages

    def attack(self, from_char, to_char):
        """ Perform an attack represented by self from from_char to to_char."""

        print self.messages['prep_msg'] % (from_char.desc['job'],
                                           to_char.desc['job'],
                                           self.wpn_name)

        # calculate hit
        # Hit formula:
        #   1d20 + attribute vs defender's AC
        #   roll 20 for crit
        print "Calculating hit chance:",
        attribute = from_char.effective_stats[self.attribute]
        hit_roll, crit_roll = roll(HIT_ROLL, True)
        hit_against = to_char.effective_stats['AC']
        hit = attribute + hit_roll
        print "%d against %d" % (hit, hit_against)
        
        # calculate damage
        # Dmg formula:
        #   roll 20 and > enemy's AC = max dmg
        #   roll 20 and < enemy's AC = regular dmg
        #   roll 1 = 0 dmg
        #   noncrit roll and < enemy's AC = 0 dmg
        #
        #   dmg = dmg roll + attacker's weapon attribute (dex or str)

        # critical hit roll
        if hit_roll == crit_roll:
            # crit and successful hit, max damage
            if hit > hit_against:
                dmg = attribute + roll(self.dmg_roll, True)[1] 
                print "Critical! Max Damage!"
                print self.messages['hit_crit_msg']
                print to_char.update_hp(-dmg)
            # crit but not enough to hit, regular damage
            else:
                dmg = attribute + roll(self.dmg_roll, False)[0] 
                print "Critical!"
                print self.messages['hit_success_msg']
                print to_char.update_hp(-dmg)
        # noncritical hit roll, but beats enemy's AC
        elif hit > hit_against:
            print self.messages['hit_success_msg']
            print "Calculating damage:",
            dmg = attribute + roll(self.dmg_roll, True)[0] 
            print to_char.update_hp(-dmg)
        else:
            print self.messages['hit_fail_msg']

