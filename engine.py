""" This module contains the Engine class (game engine)."""

from sys import exit


class Engine(object):
    """ The game engine that gets and runs the next scene from the map."""

    def __init__(self, scene_map):
        """ Initialize the engine with an existing game map."""
        self.scene_map = scene_map

    def play(self):
        """ Start playing the game by entering the opening scene."""
        current_scene = self.scene_map.opening_scene()
        while True:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

    def arena(self):
        """ Start arena mode."""
        print "Entering the arena!"
        exit(1)
