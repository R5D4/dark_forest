"""
This module provides the map and the scenes of the map.

Contains the Map class.
Contains the Scene class and all special scene subclasses.
"""

from sys import exit
from random import randint
import char
import combat
import map_gen
import draw_map
import game_clock


##########  CONSTANTS ##########

ENV_ACTIONS = {
    'look': ['l', 'look'],
    'map': ['m', 'map'],
    'time': ['t', 'time'],
    'wait': ['wait'],
    'rest': ['r', 'rest'],
    'sleep': ['sleep'],
    'pray': ['p', 'pray'],
    'stats': ['stats'],
    'inventory': ['i', 'inventory'],
    'equip': ['q', 'equip'],
    'unequip': ['u', 'unequip'],
    'examine': ['x', 'examine'],
    'search': ['search'],
    'take': ['take'],
    'help': ['h', 'help']
}

# action durations in hours
ACTION_DURATION = {
                    # travel always take one clock tick
                    'wait': 1,
                    'rest': 3,
                    'sleep': 8,
                    'pray': 1,
                    'search': 1
                  }

# make single list of supported actions to check against user action
SUPPORTED_ACTIONS = \
    [ ele for key in ENV_ACTIONS.keys() for ele in ENV_ACTIONS[key] ]

ENCOUNTER_BASE = 1 # 1% base encounter chance
# time-based bonus for encounter chance (%)
ENCOUNTER_TIME = { 
                 'sunrise': 2,
                 'dawn': 1,
                 'dusk': 1,
                 'sundown': 2,
                 'night1': 3,
                 'midnight': 3,
                 'night2': 3 
                 }

# environment-based bonus for encounter chance (%)
ENCOUNTER_ENV = {
                'wallow': 10,
                'rooting': 4,
                'damaged_tree': 3,
                'dead_wood': 2, 
                'bed': 5, 
                'track': 5
                }

##########  MAP CLASS  ##########


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
        """ Create player character."""
        print "\nRolling player character:"
        print "-" * 20
        player = char.Player()
        print player.get_stats()
        self.characters['player'] = player

    def add_boar(self):
        """ Create boss character."""
        print "\nRolling boss character:"
        print "-" * 20
        boar = char.Boar()
        print boar.get_stats()
        self.characters['boar'] = boar

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

##########  SCENE CLASS  ##########


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
            'encounter_chance': ENCOUNTER_BASE,
            'encounter': False,
            'can_leave': True 
        }
        self.features = [] # Feature objects
        self.items = [] # uncovered items player can pick up
        self.description = "No description available."

    def enter(self):
        """
        Execute actions upon entering a scene.
        """
        # 1. Print scene description
        self.describe()

        # 2. Calculate encounter chance and print encounter message
        e_chance = self.update_encounter()
        print "Encounter chance is {}".format(e_chance)
        self.print_encounter_msg()
        # if the boss attacks, go into combat directly 
        if self.get_boss_attack():
            print "The boar notices you and charges!"
            return combat.begin_combat(self.characters, self, True)

        # 3. Enter user-input loop
        while True:
            action = raw_input("> ")
            # exit scene
            if action in self.exits.keys() and self.flags['can_leave']:
                self.clock_tick()
                return self.exits.get(action) 
            # enter combat
            elif combat.ATTACK in action and self.flags['encounter']:
                return combat.begin_combat(self.characters, self, True)
            # map commands
            else: 
                self.process_action(action)
                self.print_encounter_msg() # print encounter msg after action
                if self.get_boss_attack():
                    print "The boar notices you and charges!"
                    return combat.begin_combat(self.characters, self, True)

    def process_action(self, r_action):
        """ Process user action that doesn't change scenes."""
        # The ' '.join and split() ensures only one space between each word.
        # Then we add another space to make sure we can always unpack 
        # into two vars.
        action, args = (' '.join(r_action.split())+' ').split(' ', 1)
        args = args.strip()
        player = self.characters['player']
        
        if action in SUPPORTED_ACTIONS:
            if action in ENV_ACTIONS['look']:
                self.describe()
                self.print_items()
            elif action in ENV_ACTIONS['map']:
                self.scene_map.draw_map(self.location)
            elif action in ENV_ACTIONS['time']:
                print "Time is {}:00".format(self.scene_map.clock.time)
            elif action in ENV_ACTIONS['wait']:
                print "You wait."
                print self.clock_tick()
            elif action in ENV_ACTIONS['rest']:
                print self.cmd_rest()
            elif action in ENV_ACTIONS['sleep']:
                print self.cmd_sleep()
            elif action in ENV_ACTIONS['pray']:
                print "You offer a prayer to Elbereth."
                print self.clock_tick()
            elif action in ENV_ACTIONS['stats']:
                print player.get_stats()
            elif action in ENV_ACTIONS['inventory']:
                print player.get_inventory()
            elif action in ENV_ACTIONS['equip']:
                print self.equip(args)
            elif action in ENV_ACTIONS['unequip']:
                print self.unequip(args)
            elif action in ENV_ACTIONS['examine']:
                print self.examine(args)
            elif action in ENV_ACTIONS['search']:
                print self.search()
                print self.clock_tick()
            elif action in ENV_ACTIONS['take']:
                print self.take(args)
            elif action in ENV_ACTIONS['help']:
                print self.print_help()
        else:
            print "You can't do that."

    ##### Command Methods ##### 

    def cmd_rest(self):
        """ Execute 'rest' command. Return output string."""
        n = ACTION_DURATION['rest']
        player = self.characters['player']
        msg = ["You take a rest ({} hrs).".format(n)]
        # loop until command finished or boss encountered
        for i in xrange(n):
            if self.flags['encounter']:
                msg.append("You are woken up by a noise!")
                break
            msg.append(player.rest())
            msg.append(self.clock_tick())
        return '\n'.join(msg)

    def cmd_sleep(self):
        """ Execute 'sleep' command. Return output string."""
        n = ACTION_DURATION['sleep']
        player = self.characters['player']
        msg = ["You set up camp for a well-deserved rest ({} hrs).".format(n)]
        # loop until command finished or boss encountered
        for i in xrange(n):
            if self.flags['encounter']:
                msg.append("You are woken up by a noise!")
                break
            msg.append(player.sleep())
            msg.append(self.clock_tick())
        return '\n'.join(msg)
        
    def take(self, args):
        """ Take an item from the scene. Return output string."""
        player = self.characters['player']
        if not args:
            message = "Please indicate item ID."
        else:
            item = None
            try:
                item = self.items[int(args)]
            except:
                return "No such item."
            if item is not None:
                # add item to inventory
                player.pick_up(item)
                # remove item from scene
                self.items.remove(item)
                message = "Took {}.".format(item.desc['name'])
        return message

    def search(self):
        """ Search the scene and uncover items. Return output string."""
        uncovered = [] # list of all uncovered items from all item stashes
        # search all item stashes in this scene
        for f in self.features:
            if isinstance(f, ItemStash):
                uncovered.extend(f.search())
        # add uncovered items to scene.items
        self.items.extend(uncovered)
        # return a nice message
        msg = ["You spend some time searching."]
        if uncovered: # not empty
            msg.append("Uncovered the following items:")
            for item in uncovered:
                msg.append(item.desc['name'])
        else:
            msg.append("You found nothing.")
        return '\n'.join(msg)

    def print_help(self):
        """ Return output string containing all commands and shortcuts."""
        message = []
        for cmd, keywords in ENV_ACTIONS.items():
            message.append("{}: {}".format(cmd, keywords))
        return '\n'.join(message)

    def examine(self, args):
        """ Examine an item in player inventory. Return output string."""
        player = self.characters['player']
        if not args:
            message = "Please indicate inventory item ID."
        else:
            item = None
            try:
                item = player.inventory[int(args)]
            except:
                return "No such item."
            if item is not None:
                message = item.get_info()
        return message

    def unequip(self, args):
        """ Process the 'unequip' command. Return output string."""
        player = self.characters['player']
        # if no arguments specified, return error message
        if not args or args not in player.equipped:
            message = "Please indicate slot to unequip. E.g. 'unequip R_hand'"
        else:
            message = player.unequip(args)
        return message

    def equip(self, args):
        """ Process the 'equip' command. Return output string if applicable."""
        out_str = ''
        player = self.characters['player']
        if not args: # no argument, print equipped items
            out_str = player.get_equipped()
        else: # trying to equip something
            item = None
            # check if args represents a proper index
            try: 
                item = player.inventory[int(args)]
            except: # catch everything
                return "No such item."
            out_str = player.equip(item)
        return out_str
    
    ##### Helper Methods #####

    def describe(self): 
        """
        Print a description of the scene.
        """
        print '-' * 40
        print self.description

    def print_items(self):
        """ Print list of accessible items in the scene if any."""
        if self.items:
            msg = ["You see the following items:"]
            for item in self.items:
                msg.append("{} {}".format(self.items.index(item),
                                          item.desc['name']))
            print '\n'.join(msg)

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
        time_mod = ENCOUNTER_TIME.get(self.scene_map.clock.time_period(), 0)
        # environmental(feature) encounter bonus
        environ_mod = 0
        for f in self.features:
            environ_mod += f.get_encounter_rate()
        # signs of activity bonus
        clue_mod = 0 
        chance = base + time_mod + environ_mod + clue_mod
        # set the encounter flag to True if boss in encountered
        self.flags['encounter'] = randint(1,100) <= chance
        # for diagnostic
        return chance

    def clock_tick(self):
        """
        Advance the clock by one tick. Return encounter chance message."

        Update time-based flags. Recalculates encounter chance.
        """
        self.scene_map.clock.tick()
        return "Encounter chance is {}".format(self.update_encounter())

    def get_boss_attack(self):
        """ Return True if boss will initiate combat. False otherwise."""
        # NOTE: Currently 50% chance boss will attack if encountered. 
        #       upgrade this algorithm..
        return self.flags['encounter'] and randint(1, 100) <= 50 

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

########## FEATURE CLASS ##########


class Feature(object):
    """ Base class for a scene feature."""

    def __init__(self):
        pass

    def get_desc(self):
        """ Return feature description."""
        return "No feature description. Override this method."

    def get_encounter_rate(self):
        """Return this feature's contribution to encounter rate."""
        return 0

########## FEATURE SUBCLASSES ##########


class ItemStash(Feature):
    """ An item stash."""

    def __init__(self, items):
        """ items is list of Item objects."""
        self.hidden_items = items
        
    def get_desc(self):
        """ Return feature description. Overrides Feature.get_desc"""
        return "Discarded weapons are strewn all over the ground."

    def search(self):
        """ Execute a search and return list of uncovered items."""
        chance = randint(0, 99)
        # all items with rarity below the find chance are uncovered
        d = [ i for i in self.hidden_items if uncover(i, chance) ]
        # remove uncovered items from hidden items
        self.hidden_items = \
            [ i for i in self.hidden_items if not uncover(i, chance) ]
        return d


class Stratum(Feature):
    """ A forest stratum."""

    def __init__(self, stratum, flora):
        """
        stratum is string e.g. 'canopy'
        flora is list of strings describing plants in the stratum
        """
        self.stratum = stratum
        self.flora = flora

    def get_desc(self):
        """ Return feature description. Overrides Feature.get_desc"""
        return "The {} is {}.".format(self.stratum, self.flora)


class Landmark(Feature):
    """ A landmark indicating boss activity."""

    def __init__(self, landmark_type, landmark_desc):
        """
        landmark_type is string rep. type of landmark e.g. wallow
        landmark_desc is string rep description of landmark
        """
        self.l_type = landmark_type
        self.l_desc = landmark_desc

    def get_desc(self):
        """ Return feature description. Overrides Feature.get_desc"""
        return "The {} is {}.".format(self.l_type, self.l_desc)

    def get_encounter_rate(self):
        """
        Return feature's encounter rate. 

        Overrides Feature.get_encounter_rate
        """
        return ENCOUNTER_ENV[self.l_type]

########## HELPER FUNCTIONS ##########


def uncover(item, chance):
    """ Return True if a search with the specified chance would
    uncover the item. Otherwise return False."""
    return item.desc['rarity'] <= chance
