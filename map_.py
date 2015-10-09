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
import game_clock


BASE_ENCOUNTER = 1 # 1% base encounter chance
# time-based bonus for encounter chance (%)
TIME_ENCOUNTER = { 
                 'sunrise': 2,
                 'dawn': 1,
                 'dusk': 1,
                 'sundown': 2,
                 'night1': 3,
                 'midnight': 3,
                 'night2': 3 
                 }


class Map(object):
    """
    A game map. 
    
    Contains scenes, characters, and various methods.
    """

    def __init__(self, start_scene_name):
        """ Set start scene name, create characters, create scene objects."""
        self.start_scene_name = start_scene_name
        self.scenes = {}
        self.special_scenes = {}
        self.characters = {};
        self.clock = game_clock.GameClock()


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

    def add_scene(self, scene):
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

    def draw_map(self, current_loc):
        """ Draw the map in ASCII graphics."""
        draw_map.print_canvas(draw_map.prepare_canvas(self, current_loc))


class Scene(object):
    """ Defines a generic scene."""

    def __init__(self, characters):
        """
        Set default attributes.
        """
        self.scene_map = None # the map to which this scene belongs
        self.name = None
        self.location = None
        self.characters = characters
        self.exits = {}
        self.flags = {
            'encounter_chance': BASE_ENCOUNTER,
            'encounter': False,
            'can_leave': True 
        }
        self.features = {}
        self.description = "No description available."

    def process_action(self, action):
        """ Process user action that doesn't change scenes."""
        ENV_ACTIONS = {
            'look': ['l', 'look'],
            'map': ['m', 'map'],
            'time': ['t', 'time'],
            'wait': ['wait'],
            'rest': ['r', 'rest'],
            'pray': ['p', 'pray']
        }
        # make single list of supported actions to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
            elif action in ENV_ACTIONS['map']:
                self.scene_map.draw_map(self.location)
            elif action in ENV_ACTIONS['time']:
                print "Time is {}:00".format(self.scene_map.clock.time)
            elif action in ENV_ACTIONS['wait']:
                print "You wait for 1 hour."
                self.advance_clock('wait')
                self.update_encounter()
            elif action in ENV_ACTIONS['rest']:
                print "You rest for 3 hours."
                self.advance_clock('rest')
                self.update_encounter()
            elif action in ENV_ACTIONS['pray']:
                print "You offer a prayer to Elbereth (1 hour)."
                self.advance_clock('pray')
                self.update_encounter()
        else:
            print "You can't do that."

    def describe(self): 
        """
        Print a description of the scene.
        """
        print '-' * 40
        print self.description
    
    def print_encounter_msg(self):
        """ Print a message indicating if the boss is in the area."""
        if self.flags['encounter']:
            print "You see the boar! You don't think it notices you."

    def update_encounter(self):
        """
        Determine if player encounters the boss and print a message.

        Only recalculate after time has passed.
        """
        # Calculate encounter chance
        base = self.flags['encounter_chance']
        time_mod = TIME_ENCOUNTER.get(self.scene_map.clock.time_period(), 0)
        environ_mod = 0 # environmental bonus
        clue_mod = 0 # signs of activity bonus
        chance = base + time_mod + environ_mod + clue_mod
        print "Encounter chance: {}".format(chance)
        # Determine if boss is encountered
        self.flags['encounter'] = randint(1,100) <= chance
        # Print encounter message
        self.print_encounter_msg()

    def advance_clock(self, action):
        """ 
        Advance the clock by duration of action
        """
        self.scene_map.clock.advance_time(action)

    def enter(self):
        """
        Execute actions upon entering a scene.
        """
        # 1. Print scene description
        self.describe()

        # 2. Calculate encounter chance and print encounter message
        self.update_encounter()

        # 3. Enter user-input loop
        while True:
            action = raw_input("> ")
            if action in self.exits.keys() and self.flags['can_leave']:
                self.advance_clock('travel')
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

