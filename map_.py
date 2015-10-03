"""
This module provides the map and the scenes of the map.

Contains the Map class.
Contains the generic Scene class and all map area scene subclasses.
"""

from sys import exit
from random import randint
import char
import combat
import map_gen
import draw_map


class Map(object):
    """
    Defines the map. 

    Instance variables:
        self.characters
        self.scenes
        self.special_scenes
        self.start_scene_name
    Methods:
        __init__(self, start_scene_name)
        next_scene(self, scene_name)
        opening_scene(self)
        roll_characters(self)
    """

    def __init__(self, start_scene_name):
        """ Set start scene name, create characters, create scene objects."""
        self.start_scene_name = start_scene_name
        self.scenes = {}
        self.special_scenes = {}
        self.characters = {};

    def next_scene(self, scene_name):
        """ Return the Scene object for the next scene."""
        if scene_name in self.scenes:
            return self.scenes.get(scene_name)
        elif scene_name in self.special_scenes:
            return self.special_scenes.get(scene_name)

    def opening_scene(self):
        """ Return the Scene object for the opening scene."""
        return self.next_scene(self.start_scene_name)

    def add_characters(self):
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

    def add_scene(self, name, scene):
        """ Add a scene to the map with 'name' as the key to the dict."""
        scene.scene_map = self
        self.scenes.update({scene.name: scene})

    def add_special_scene(self, name, scene):
        """ Add a special scene."""
        self.special_scenes.update({name: scene})

    def print_map(self):
        """ Print out the map by printing each scene's exits."""
        for scene in self.scenes.values():
            print "name: {}, location: {}".format(scene.name, scene.location)
            print "    exits: {}".format(scene.exits)

    def draw_map(self):
        """ Draw the map in ASCII graphics."""
        draw_map.print_canvas(draw_map.prepare_canvas(self))


class Scene(object):
    """ Defines a generic scene."""

    def __init__(self, characters):
        """
        Set default attributes.
        """
        self.scene_map = None # the map to which this scene belongs
        self.name = None
        self.location = ()
        self.characters = characters
        self.exits = {}
        self.flags = {
            'encounter_chance': 0,            
            'encounter': False,
            'can_leave': True 
        }
        self.features = {}
        self.description = "No description available."

    def process_action(self, action):
        """ Process user action."""
        ENV_ACTIONS = {
            'look': ['l', 'look'],
            'map': ['m', 'map']
        }
        # make single list of supported actions to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
            elif action in ENV_ACTIONS['map']:
                self.scene_map.draw_map()
        else:
            print "You can't do that."

    def describe(self): 
        """
        Print a description of the scene.
        """
        print self.description
    
    def print_encounter_msg(self):
        """ Print a message indicating if the boss is in the area."""
        if self.flags['encounter']:
            print "You see the boar! You don't think it notices you."

    def encounter(self, chance):
        """
        Calculate and return if the player has encountered the boss.

        chance: encounter probability in (0, 1).
        return True or False.
        """
        return randint(1,10) <= (chance * 10)

    def enter(self):
        """
        Execute actions upon entering a scene.
        """
        # 1. Print scene description
        self.describe()

        # 2. Calculate encounter chance and print encounter message
        chance = self.flags['encounter_chance']
        self.flags['encounter'] = self.encounter(chance)
        self.print_encounter_msg()
        
        # 3. Enter user-input loop
        while True:
            action = raw_input("> ")
            # trying to leave
            if action in self.exits.keys() and self.flags['can_leave']:
                return self.exits.get(action) 
            elif combat.ATTACK in action and self.flags['encounter']:
                return combat.begin_combat(self.characters)
            else: 
                self.process_action(action)


##########  SPECIAL SCENES  ##########


class Death(Scene):
    """ Special scene for dying. No interaction. Game over."""

    def enter(self):
        print "\n\n"
        print '*' * 30
        print "Your vision fades as the warmth drains out of you from your"
        print "wounds... Damn... so that's where I put my keys... hurk!"
        print '*' * 20,
        print "GAME OVER",
        print '*' * 20
        print "Please support my kickstarter campaign for more content!"
        exit(1)


class Win(Scene):
    """ Special scene for winning. No interaction. You're a winner."""

    def enter(self):
        print "\n\n"
        print '*' * 30
        print "You SMOTE the boar on the forest floor!"
        print "Wait 'til the lads hear about this!"
        print "Time to get the hell outta here."
        print '*' * 20,
        print "GAME OVER",
        print '*' * 20
        print "Please support my kickstarter campaign for more content!"
        exit(1)


class Quit(Scene):
    """ Special scene for quitting. No interaction. Game over."""

    def enter(self):
        print "\n\n"
        print '*' * 30
        print "You breathe a sigh of relief as you exit the oppressive"
        print "atmosphere of the forest. But what are you going to tell"
        print "the others? Damn, this is like ranger school all over again!"
        print "You slowly start on your long journey back to the village."
        print '*' * 20,
        print "GAME OVER",
        print '*' * 20
        print "Please support my kickstarter campaign for more content!"
        exit(1)


class Story(Scene):
    """ Special scene to print the story. Should be first scene in map."""
    
    def describe(self):
        print "\n\n"
        print '*' * 30,
        print "WELCOME",
        print '*' * 30

        print "An evil wakes in the East. You've seen a growing number of"
        print "wild beasts scavenging near your small village located"
        print "just south of the Dark Forest."
        print "Recently, an unusally large and ferocious wild boar has been"
        print "getting into the fields, destroying everything that it cannot"
        print "eat."
        print "As the only ranger in your village, you've reluctantly"
        print "accepted the task of getting rid of this foul beast."
        print "You've tracked the animal to the edge of the Dark Forest."
        print "You enter into the shadow of the trees..."

    def enter(self):
        """ Print description and return first map area scene."""
        self.describe()
        return 'entrance'

