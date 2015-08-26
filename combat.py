# module to handle combat

from random import randint
from random import choice
import char

# user types this to signal attack
ATTACK = 'attack'


# Combat! Yay!
# returns either 'death' or 'win'
# no running! battle to the death
def begin_combat(characters):

    player = characters['player']
    boar = characters['boar']

    print "*" * 10,
    print " Entering combat! ",
    print "*" * 10
    
    ########## INITIATIVE ##########

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

    ########## COMBAT LOOP ##########
    while True:
        print '-' * 20
        if turn == 'player':
            print "Player's turn:"
            print "HP: %d" % player.attributes['HP']
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
            #print "HP: %d" % boar.attributes['HP']
            # output bloodied message if HP < 30%
            if boar.attributes['HP']/float(boar.attributes['max_HP']) < 0.3:
                print "The boar is bloodied!"
            boar_attack = boar.attacks[choice(boar.attacks.keys())]
            boar_attack.attack(boar, player)
            turn = 'player'
        
        if player.attributes['HP'] <= 0:
            return 'death' 
        elif boar.attributes['HP'] <= 0:
            return 'win' 


# Parses the dice roll formatting string
def parse_roll(formatting):
    extracted = formatting.split('d')
    times = int(extracted[0])
    die_max = int(extracted[1])
    #print "extracted: times = %d, die_max = %d" % (times, die_max)
    return (times, die_max)
    

# Roll dice of the specified type and number of times
# e.g. '1d20' will simulate rolling a 20-sided die (1-20) once
# '2d6' will simulate rolling a 6-sided die (1-6) twice
# output = True will output dice roll details, False will be silent
def roll(formatting, output):
    if output:
        print "Rolling %s..." % formatting,
    times, die_max = parse_roll(formatting)
    total = 0
    max_roll = 0
    for i in range(1, times+1):
        total += randint(1, die_max)
        max_roll += die_max
    if output:
        print "%d!" % total
    return (total, max_roll)


# holds information about an attack
class Attack(object):

    def __init__(self):
        # override this
        self.details = {
            'prep_msg': None,
            'hit_crit_msg': None,
            'hit_success_msg': None,
            'hit_fail_msg': None,
            'hit_attr': None,
            'hit_roll': None,
            'hit_against': None,
            'dmg_roll': None,
            'dmg_base': None
        }


    # attack from <from_char> to <to_char>
    # Hit formula: hit if (<from_char>.<hit_attr> + <hit_roll>)
    #                     > (<to_char>.<hit_againt>)
    # Dmg formula: <dmg>
    def attack(self, from_char, to_char):
        print self.details['prep_msg'] % (from_char.desc['job'], 
                                      to_char.desc['job'])
        # calculate hit
        print "Calculating hit chance:",
        hit_attr = from_char.attributes[self.details['hit_attr']]
        hit_roll, crit_roll = roll(self.details['hit_roll'], True)
        hit_against = to_char.attributes[self.details['hit_against']]
        hit = hit_attr + hit_roll
        print "%d against %d" % (hit, hit_against)
        
        # damage calculation
        if hit_roll == crit_roll:
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


class Slash(Attack):
    
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


class Shoot(Attack):
    
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


class Stab(Attack):
    
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


class Charge(Attack):
    
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


class Kick(Attack):
    
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


class Bite(Attack):
    
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

