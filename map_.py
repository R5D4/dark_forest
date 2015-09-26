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


class Map(object):
    """
    Defines the map. 

    Instance variables:
        self.characters
        self.scenes
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
        self.characters = {};

    def next_scene(self, scene_name):
        """ Return the Scene object for the next scene."""
        return self.scenes.get(scene_name)

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
        self.scenes.update({name: scene})

    def print_map(self):
        """ Print out the map."""
        for scene in self.scenes.values():
            print "{}: ".format(scene.name)
            print "    exits: {}".format(scene.exits)


class Scene(object):
    """ Defines a generic scene."""

    def __init__(self, characters):
        """
        Set default attributes.
        """
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
        }
        # make single list of supported actions to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
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


##########  MAP AREA SCENES ##########


class StartArea(Scene):
    """ Area 1. name = 'start_area'."""

    def __init__(self, characters):
        super(StartArea, self).__init__(characters)
        # add exits
        self.exits['ne'] = 'dead_log_area'
        self.exits['se'] = 'ponds_area'
        # add flags
        self.flags['encounter_chance'] = 0.1
        self.flags['on_tree'] = False

    def process_action(self, action):
        """ Override Scene.process_action"""
        ENV_ACTIONS = {
            'look': ['l', 'look'],
            'up': ['up', 'climb up'],
            'down': ['down', 'climb down']
        }
        # make single list of supported actions to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
            elif action in ENV_ACTIONS['up']:
                if not self.flags['on_tree']:
                    print "You climb the tall oak."
                    self.flags['on_tree'] = True
                    self.flags['can_leave'] = False
                else:
                    print "You're already at the top!"
            elif action in ENV_ACTIONS['down']:
                if self.flags['on_tree']:
                    print "You climb down the tree."
                    self.flags['on_tree'] = False
                    self.flags['can_leave'] = True 
                else: 
                    print "You're already on the ground."
        else:
            print "You can't do that."

    # print description of surroundings
    def describe(self):
        print '-' * 20
        if self.flags['on_tree']:
            print "You peek out of the top of the tree and look out."
            print "The forest is deep and dark. There are some ponds to the"
            print "South-East and a small clearing further in that direction."
        else:
            print "This is where you entered the forest." 
            print "There's a giant oak tree. It has rough bark and strong"
            print "branches. You think you can climb it."
            print "The animal trail leads North-East (ne) and South-East (se)."


class DeadLogArea(Scene):
    """ Area 2. name = 'dead_log_area'."""

    def __init__(self, characters):
        super(DeadLogArea, self).__init__(characters)
        # add exits
        self.exits['sw'] = 'start_area'
        self.exits['e'] = 'dead_end'
        self.exits['se'] = 'brook_area'
        # add flags
        self.flags['encounter_chance'] = 0.2

    def process_action(self, action):
        """ Override Scene.process_action"""
        ENV_ACTIONS = {
            'look': ['l', 'look'],
        }
        # make single list of supported actions to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "Small broken logs and branches are scattered all across the"
        print "animal trail in this area; probably the result of a big storm."
        print "You find it difficult to move around very quickly."
        print "The animal trail leads South-West (sw), East (e), and"
        print "South-East (se)."


class PondsArea(Scene):
    """ Area 3. name = 'ponds_area'."""

    def __init__(self, characters):
        super(PondsArea, self).__init__(characters)
        # add exits
        self.exits['nw'] = 'start_area'
        self.exits['e'] = 'tall_tree_area'
        self.exits['se'] = 'glade_area'
        # add flags
        self.flags['encounter_chance'] = 0.3
    
    def process_action(self, action):
        """ Override Scene.process_action"""
        ENV_ACTIONS = {
            'look': ['l', 'look']
        }
        # make single list of supported actions to check against user action 
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "The animal trail is flanked by tall reeds on both sides."
        print "Through the dense vegetation you can make out clear ponds."
        print "The trail is very narrow here."
        print "The animal trail leads North-West (nw), East (e), and"
        print "South-East (se)."


class DeadEnd(Scene):
    """ Area 4. name = 'dead_end'."""

    def __init__(self, characters):
        super(DeadEnd, self).__init__(characters)
        # add exits
        self.exits['w'] = 'dead_log_area'
        # add flags
        self.flags['encounter_chance'] = 0.3
    
    def process_action(self, action):
        """ Override Scene.process_action"""
        ENV_ACTIONS = {
            'look': ['l', 'look']
        }
        # make a single list of supported action to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]

        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "The animal trail ends abruptly ahead. There doesn't seem to be"
        print "any paths other than the on which you came."
        print "The animal trail leads West (w)."


class BrookArea(Scene):
    """ Area 5. name = 'brook_area'."""

    def __init__(self, characters):
        super(BrookArea, self).__init__(characters)
        # add exits
        self.exits['nw'] = 'dead_log_area'
        self.exits['s'] = 'tall_tree_area'
        # add flags
        self.flags['encounter_chance'] = 0.5
    
    def process_action(self, action):
        """ Override Scene.process_action."""
        ENV_ACTIONS = {
            'look': ['l', 'look']
        }
        # Make a single list of supported actions to check against user action.
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]

        if action in ENV_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "There is a shallow brook ahead as the vegetation thins."
        print "Yet you can only barely make out the sky through"
        print "the thick dark canopy."
        print "The animal trail leads North-West (nw) and South (s)."


class TallTreeArea(Scene):
    """ Area 6. name = 'tall_tree_area'."""

    def __init__(self, characters):
        super(TallTreeArea, self).__init__(characters)
        # add exits
        self.exits['n'] = 'brook_area'
        self.exits['w'] = 'ponds_area'
        self.exits['s'] = 'glade_area'
        self.exits['e'] = 'exit_e'
        # add flags
        self.flags['encounter_chance'] = 0.4
        self.flags['on_tree'] = False
    
    def process_action(self, action):
        """ Override Scene.process_action."""
        ENV_ACTIONS = {
            'look': ['l', 'look'],
            'up': ['up', 'climb up'],
            'down': ['down', 'climb down']
        }
        # make single list of supported actions to check against user action
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
            elif action in ENV_ACTIONS['up']:
                if not self.flags['on_tree']:
                    print "You climb the tree."
                    self.flags['on_tree'] = True
                    self.flags['can_leave'] = False
                else:
                    print "You're already at the top!"
            elif action in ENV_ACTIONS['down']:
                if self.flags['on_tree']:
                    print "You climb down the tree."
                    self.flags['on_tree'] = False
                    self.flags['can_leave'] = True 
                else: 
                    print "You're already on the ground."
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        if self.flags['on_tree']:
            print "It takes you a while to climb out of the canopy of the"
            print "forest. There are some ponds to the North-West and"
            print "you see a clearing just a short distance to the south."
            print "Looking East, you can see the edge of the forest."     
        else:
            print "There are many fir trees in this area. But one in"
            print "particular looks, taller, stronger, and more ancient than"
            print "the others."
            print "You could probably get a nice view of the surroundings"
            print "if you climbed it."
            print "The animal trail leads North (n), West (w), South (s) and"
            print "East (e)."


class GladeArea(Scene):
    """ Area 7. name = 'glade_area'."""

    def __init__(self, characters):
        super(GladeArea, self).__init__(characters)
        # add exits
        self.exits['n'] = 'tall_tree_area'
        self.exits['nw'] = 'ponds_area'
        self.exits['w'] = 'exit_sw'
        # add flags
        self.flags['encounter_chance'] = 0
    
    def process_action(self, action):
        """ Override Scene.process_action."""
        ENV_ACTIONS = {
            'look': ['l', 'look']
        }
        # Make a single list of supported actions to check against user action.
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]

        if action in ENV_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "It's a beautiful glade! For reasons entirely unknown to you,"
        print "the trees open up a wide circle roughly 10 meters across."
        print "In the middle is a green meadow dotted by small yellow flowers."
        print "As you enter the meadow, you feel warm and safe. Beasts of The"
        print "Enemy probably would not stray near."
        print "The animal trail leads North (n), North-West (nw) and West (w)."


class ExitSW(Scene):
    """ Area 8. name = 'exit_sw'."""

    def __init__(self, characters):
        super(ExitSW, self).__init__(characters)
        # add exits
        self.exits['e'] = 'glade_area'
        self.exits['w'] = 'quit'
        # add flags
        self.flags['encounter_chance'] = 0.4
    
    def process_action(self, action):
        """ Override Scene.process_action."""
        ENV_ACTIONS = {
            'look': ['l', 'look']
        }
        # Make a single list of supported actions to check against user action.
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]

        if action in ENV_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "The forest feels less gloomy and you think you see light"
        print "filtering through the tree trunks up ahead. Following the"
        print "path for a bit, you see an exit!"
        print "The animal trail leads East (e) and West (w) out of the forest."


class ExitE(Scene):
    """ Area 9. name = 'exit_e'."""

    def __init__(self, characters):
        super(ExitE, self).__init__(characters)
        # add exits
        self.exits['w'] = 'tall_tree_area'
        self.exits['e'] = 'quit'
        # add flags
        self.flags['encounter_chance'] = 0.4
    
    def process_action(self, action):
        """ Override Scene.process_action."""
        ENV_ACTIONS = {
            'look': ['l', 'look']
        }
        # Make a single list of supported actions to check against user action.
        SUPPORTED_ACTIONS = \
            [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]

        if action in ENV_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_encounter_msg()
        else:
            print "You can't do that."

    def describe(self):
        print '-' * 20
        print "The forest feels less gloomy and you think you see light"
        print "filtering through the tree trunks up ahead. Following the"
        print "path for a bit, you see an exit!"
        print "The animal trail leads West (w) and East (e) out of the forest."

