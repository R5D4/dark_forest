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
            self.characters['player'] = char.Player()
            response = raw_input("Reroll character? (y/n): ")

    def add_boar(self):
        """ Create boss character. Allow user to re-roll."""
        response = 'y'
        while response == 'y':
            print "\nRolling boss character:"
            print "-" * 20
            self.characters['boar'] = char.Boar()
            response = raw_input("Reroll character? (y/n): ")

    def enter(self):
        """ Enter the arena and start combat."""
        combat.begin_combat(self.characters)
