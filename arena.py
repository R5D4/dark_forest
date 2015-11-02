"""
This module provides the Arena class.
"""

import char
import combat

class Arena(object):
    """
    Defines an arena.
    """

    def __init__(self):
        self.characters = {}
        self.add_player()
        self.add_boar()

    def add_player(self):
        """ Create player character. Allow user to re-roll."""
        response = 'y'
        while response == 'y':
            print "\nRolling player character:"
            print "-" * 20
            player = char.Player()
            print player.get_stats()
            response = raw_input("Reroll character? (y/n): ")
            self.characters['player'] = player

    def add_boar(self):
        """ Create boss character. Allow user to re-roll."""
        response = 'y'
        while response == 'y':
            print "\nRolling boss character:"
            print "-" * 20
            boar = char.Boar()
            print boar.get_stats()
            response = raw_input("Reroll character? (y/n): ")
            self.characters['boar'] = boar

    def enter(self):
        """ Enter the arena and start combat."""
        result = combat.begin_combat(self.characters, None, False)
        if result == 'death':
            print "u ded"
        elif result == 'win':
            print "u a winnar"

