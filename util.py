"""
Contains functions that are used in multiple modules.
"""

from random import randint

FULL_DIR = {
    'n': 'north',
    'ne': 'northeast',
    'e': 'east',
    'se': 'southeast',
    's': 'south',
    'sw': 'southwest',
    'w': 'west',
    'nw': 'northwest'
}


def parse_roll(formatting):
    """
    Parse the dice roll formatting string. 

    Return the number of dice rolls and the type of die as a tuple:
    e.g. parse_roll('2d10') -> (2, 10)
    """
    extracted = formatting.split('d')
    n = int(extracted[0])
    die_max = int(extracted[1])
    #print "extracted: n = %d, die_max = %d" % (n, die_max)
    return (n, die_max)
    

def roll(formatting, output):
    """
    Roll the specified number of dice of a certain type.

    e.g. '1d20' rolls a 20-sided die.
         '2d6' rolls two 6-sided dice.
    Return the sum of the rolled dice and the maximum sum possible as a tuple.

    If output is True, this function prints the following message:
    e.g. 'Rolling 2d6... 10!'
    If output is False, this function prints nothing.
    """
    if output:
        print "Rolling %s..." % formatting,
    n, die_max = parse_roll(formatting)
    total = 0
    max_roll = 0
    for i in range(1, n+1):
        total += randint(1, die_max)
        max_roll += die_max
    if output:
        print "%d!" % total
    return (total, max_roll)


