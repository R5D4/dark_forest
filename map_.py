"""
This module provides the map and the scenes of the map.

Contains the Map class.
Contains the generic Scene class and all map area scene subclasses.
"""

from sys import exit
from random import randint
import char
import combat


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
        self.characters = {};
        self.add_player()
        self.add_boar()
        self.scenes = {
            'story': Story(self.characters),
            'death': Death(self.characters),
            'win': Win(self.characters),
            'quit': Quit(self.characters),
            'start_area': StartArea(self.characters),
            'dead_log_area': DeadLogArea(self.characters),
            'ponds_area': PondsArea(self.characters),
            'dead_end': DeadEnd(self.characters),
            'brook_area': BrookArea(self.characters),
            'tall_tree_area': TallTreeArea(self.characters),
            'glade_area': GladeArea(self.characters),
            'exit_sw': ExitSW(self.characters),
            'exit_e': ExitE(self.characters)
        }

    def next_scene(self, scene_name):
        """ Return the Scene object for the next scene."""
        return self.scenes.get(scene_name)

    def opening_scene(self):
        """ Return the Scene object for the opening scene."""
        return self.next_scene(self.start_scene_name)

    def add_player(self):
        """ Create player character. Allow user to re-roll."""
        response = 'y'
        while response == 'y':
            print "\nRolling player character:"
            print "-" * 20
            self.characters['player'] = char.Player(0)
            response = raw_input("Reroll character? (y/n): ")

    def add_boar(self):
        """ Create boss character. Allow user to re-roll."""
        response = 'y'
        while response == 'y':
            print "\nRolling boss character:"
            print "-" * 20
            self.characters['boar'] = char.Boar(0)
            response = raw_input("Reroll character? (y/n): ")


class Scene(object):
    """ Defines a generic scene."""

    def __init__(self, characters):
        """
        Set default attributes.

        Subclasse should _extend_ this method if the scene requires different
        attributes or values than the default.
        """
        self.characters = characters
        self.exits = {}
        self.flags = {
            'encounter_chance': 0,            
            'encounter': False,
            'can_leave': True 
        }

    def process_action(self, action):
        """
        Process user action.

        Currently needs to be overrode in a subclass. It is used to handle
        user actions to do with environmental interaction.
        """
        print "Please override this method."

    def describe(self): 
        """
        Print a description of the scene.

        Needs to be overrode in a subclass. 
        """
        print "Please override this method."
    
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

        The set of actions is the same for all interactive scenes. For
        special scenes like winning, dying, and quitting that are not
        interactive, override this method.
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
        return 'start_area'


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

    # process all the actions other than leaving the scene
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

    # process all the actions other than leaving the scene
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

    """Area 3"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'nw': 'start_area',
            'e': 'tall_tree_area',
            'se': 'glade_area'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0.3
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
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

    """Area 4"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'w': 'dead_log_area'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0.3
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
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

    """Area 5"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'nw': 'dead_log_area',
            's': 'tall_tree_area'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0.5
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
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

    """Area 6"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'n': 'brook_area',
            'w': 'ponds_area',
            's': 'glade_area',
            'e': 'exit_e'
        }
        self.flags = {
            'can_leave': True,
            'on_tree': False,
            'encounter_chance': 0.4
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l', 'climb', 'climb oak', 'climb tree',
                           'get down', 'down']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
                self.describe()
                self.print_encounter_msg()
            elif 'climb' in action and not self.flags['on_tree']:
                print "You climb the tall oak."
                self.flags['on_tree'] = True
                self.flags['can_leave'] = False
            elif 'climb' in action and self.flags['on_tree']:
                print "You're already at the top!"
            elif 'down' in action and self.flags['on_tree']:
                print "You climb down the tree."
                self.flags['on_tree'] = False
                self.flags['can_leave'] = True 
            elif 'down' in action and not self.flags['on_tree']:
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

    """Area 7"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'n': 'tall_tree_area',
            'nw': 'ponds_area',
            'w': 'exit_sw'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
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

    """Area 8"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'e': 'glade_area',
            'w': 'quit'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0.4
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
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
    """Area 9"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'w': 'tall_tree_area',
            'e': 'quit'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0.4
        }
    
    # process all the actions other than leaving the scene
    def process_action(self, action):

        ENVIRON_ACTIONS = ['l']
        
        if action in ENVIRON_ACTIONS:
            if action == 'l':
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

