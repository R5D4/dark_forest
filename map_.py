"""
This module provides the map and the scenes of the map.

Contains the Map class.
Contains the Scene class and all special scene subclasses.
"""

from sys import exit
from random import randint
from random import choice
import data.clue_data as cd
import char
import combat
import map_gen
import draw_map
import game_clock
import util


##########  CONSTANTS ##########

# available actions in a scene
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
    'search': ['search'],
    'take': ['take'],
    'drop': ['d', 'drop'],
    'equip': ['q', 'equip'],
    'unequip': ['u', 'unequip'],
    'examine': ['x', 'examine'],
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

TIME_LIMIT = 672 # roughly 28 days
# NOTE: for debugging
TIME_LIMIT =  240 # 10 days

##########  MAP CLASS  ##########


class Map(object):
    """
    A game map. 
    
    Contains scenes, characters, and various methods.
    """

    def __init__(self, start_scene_name):
        """ Set start scene name, create characters, create scene objects."""
        self.start_scene_name = start_scene_name
        self.scenes = {} # (name, Scene object)
        self.special_scenes = {} # (name, Scene object)
        self.characters = {}; # (name, Character object)
        self.lair_scene_name = None # scene name of the lair
        self.boss_scene_name = None # scene name of boss' location
        self.clock = game_clock.GameClock()
        self.path = [] # list of scene names in path (destination first)
        self.timeup = False # flag for losing due to time running out

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

    def move_boss(self):
        """
        Move the boss. 
        
        Return the pre-move scene, and movement direction or None.
        """
        direction = None
        boss_sc = self.scenes[self.boss_scene_name]
        lair = boss_sc.get_lair()
        if self.clock.is_day(): # day time, get to the lair
            # if already in lair scene, stay hidden in lair (assumed in lair)
            if self.boss_at_lair():
                pass
            else: # not in lair scene, go to lair scene
                # if no path yet, construct path
                if not self.path:
                    self.path = self.construct_path(self.boss_scene_name,
                                                    self.lair_scene_name)
                    # NOTE: print debugging statements
                    print "Constructing path to lair: {}".format(self.path)
                # move on path
                if self.path: # redundant check?
                    next_sc_name = self.path.pop()
                    next_sc = self.scenes[next_sc_name]
                    boss_sc.flags['encounter'] = False
                    next_sc.flags['encounter'] = True
                    self.boss_scene_name = next_sc_name
                    # NOTE: print debugging statements
                    direction = get_exit_dir(boss_sc, next_sc)
                    print "Moved {} from {} to {}.".format(direction, 
                                                           boss_sc.name,
                                                           next_sc_name)
                # if after moving, we are in the lair scene, hide in lair
                lair = next_sc.get_lair()
                if self.boss_at_lair() and not lair.has_boss:
                    lair.has_boss = True
                    # make boss undetectable in hidden lair
                    if not lair.revealed:
                        next_sc.flags['encounter'] = False
                    # NOTE: print debugging statements
                    print "Boss has hid in the lair."
                    
        else: # night time, move randomly
            # if in lair scene and boss in lair, get out of lair
            if self.boss_at_lair() and lair.has_boss:
                lair.has_boss = False
                # NOTE: print debugging statements
                print "Boss has left the lair."
            self.path = [] # reset path, don't need it
            direction, next_sc_name = choice(boss_sc.exits.items())
            next_sc = self.scenes[next_sc_name]
            boss_sc.flags['encounter'] = False
            next_sc.flags['encounter'] = True
            self.boss_scene_name = next_sc_name
            # NOTE: print debugging statements
            print "Moved {} from {} to {}.".format(direction, boss_sc.name,
                                                              next_sc_name)

        return (boss_sc.name, direction) 

    def boss_at_lair(self):
        """ Return True if the boss is in the lair scene. Else False."""
        return self.boss_scene_name == self.lair_scene_name

    def construct_path(self, start, goal):
        """
        Construct shortest path from start to goal.

        start: starting scene name
        goal: goal scene name
        """
        # Use BFS for now
        tree = {} # search tree: { scene_name: parent_scene_name, ... }
        queue = [] # for BFS
        visited = [] # visited scenes during BFS
        path = [] # final results

        tree[start] = None # no parent
        visited.append(start)
        queue.append(start)
        
        # construct search tree until we reach the goal
        found = False
        while queue and not found:
            current = queue.pop(0) # current scene name
            exits = self.scenes[current].exits.values()
            #  for each unvisited scene that is adjacent to current
            for adj in [ node for node in exits if node not in visited ]:
                if adj not in tree: # unvisited scene
                    tree[adj] = current # set parent
                    visited.append(adj)
                    queue.append(adj)
                # stop searching when we reach the goal
                if adj == goal:
                    found = True
                    break;

        # backtrace to construct path
        sc = goal
        while sc != start: # exclude starting scene from path
            path.append(sc)
            sc = tree[sc] # set sc to its parent

        return path

    def leave_clue(self, scene_name, direction):
        """
        Leave a clue in the given scene.
        
        scene_name: name of scene from which boss moved
        direction: direction in which the boss moved
        """
        boss_sc = self.scenes[scene_name]
        lair = boss_sc.get_lair()
        # boss is in lair = inactive. Don't leave clues.
        if lair and lair.has_boss:
            return

        # 75% chance to leave footprints on move
        if direction and randint(1, 100) <= 75: # direction not None
            boss_sc.add_clue(FootprintClue, direction)
            # NOTE: print debugging statements
            print "Left footprints in {} pointing {}.".format(scene_name, 
                                                              direction)
        if randint(1, 100) <= 20: # 30% chance to leave broken trees
            boss_sc.add_clue(BrokenTreeClue, direction)
            print "Left a broken tree in {}".format(scene_name)
        if randint(1, 100) <= 20: # 20% chance to leave slain animals
            boss_sc.add_clue(SlainAnimalClue, direction)
            print "Left a slain anmial in {}".format(scene_name)
    
    def update_clues(self):
        """ Update all clues on the map."""
        # for each clue on map, decrement freshness
        for sc in self.scenes.values():
            if sc.clues: # not None
                for clue in sc.clues:
                    clue.update()
            else: # no clues in scene
                pass

    def clock_tick(self):
        """ 
        Advance the clock by one tick.

        Perform actions that are done every clock tick.
        """
        # advance clock
        self.clock.tick()
        # if time's up, go to time up scene
        if self.clock.lifetime >= TIME_LIMIT:
            self.timeup = True
            # NOTE: debug statement
            print "Time's up!"
            return
        # boss heals when outside of combat
        boar = self.characters['boar']
        boar.heal()
        # update all clues on map
        self.update_clues()
        # move boss to different scene
        old_scene_name, direction = self.move_boss()
        # leave a clue in current scene
        self.leave_clue(old_scene_name, direction)


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
        self.exits = {} # (direction, scene_name)
        self.flags = {
            # True: potential encounter
            'encounter': False, 
            'can_leave': True 
        }
        self.features = [] # Feature objects
        self.items = [] # uncovered items player can pick up
        self.clues = [] # Clue objects
        self.description = "No description available."

    def enter(self):
        """
        Execute actions upon entering a scene.
        """
        player = self.characters['player']

        # 1. Print scene description and items
        self.cmd_look()

        # 2. Print encounter message
        self.print_encounter_msg()
        # if the boss attacks, go into combat
        if self.get_boss_attack():
            print "The boar notices you and charges!"
            return combat.begin_combat(self.characters, self, True)

        # 3. Enter user-input loop
        while True:
            action = raw_input("> ")
            # reset surprised condition since we can take an action
            player.conditions['surprised'] = False

            # exit scene
            if action in self.exits.keys() and self.flags['can_leave']:
                self.scene_map.clock_tick()
                if self.scene_map.timeup: # time's up you lose
                    return "timeup"
                return self.exits.get(action) 
            # enter combat
            elif combat.ATTACK in action and self.flags['encounter']:
                return combat.begin_combat(self.characters, self, True)
            # map commands
            else: 
                if self.process_action(action): # valid action
                    if self.scene_map.timeup: # time's up you lose
                        return "timeup"
                    self.print_encounter_msg()
                    # if the boss attacks, go into combat
                    if self.get_boss_attack():
                        print "The boar notices you and charges!"
                        return combat.begin_combat(self.characters, self, True)
                else:
                    # if invalid action, prompt for input again
                    pass

    def process_action(self, r_action):
        """
        Process user action that doesn't change scenes.
        
        Return True if the action was a valid action. False otherwise.
        """
        # The ' '.join and split() ensures only one space between each word.
        # Then we add another space to make sure we can always unpack 
        # into two vars.
        action, args = (' '.join(r_action.split())+' ').split(' ', 1)
        args = args.strip()
        player = self.characters['player']
        
        if action in SUPPORTED_ACTIONS:
            is_valid = True
            if action in ENV_ACTIONS['look']:
                self.cmd_look()
            elif action in ENV_ACTIONS['map']:
                self.scene_map.draw_map(self.location)
            elif action in ENV_ACTIONS['time']:
                print "Time is {}:00".format(self.scene_map.clock.time)
            elif action in ENV_ACTIONS['wait']:
                # advance clock by one tick
                print "You wait."
                self.scene_map.clock_tick()
            elif action in ENV_ACTIONS['rest']:
                print self.cmd_rest()
            elif action in ENV_ACTIONS['sleep']:
                print self.cmd_sleep()
            elif action in ENV_ACTIONS['pray']:
                # currently only advances the clock by one tick
                print "You offer a prayer to Elbereth."
                self.scene_map.clock_tick()
            elif action in ENV_ACTIONS['stats']:
                print player.get_stats()
            elif action in ENV_ACTIONS['inventory']:
                print player.get_inventory()
            elif action in ENV_ACTIONS['equip']:
                print self.cmd_equip(args)
            elif action in ENV_ACTIONS['unequip']:
                print self.cmd_unequip(args)
            elif action in ENV_ACTIONS['examine']:
                print self.cmd_examine(args)
            elif action in ENV_ACTIONS['search']:
                print self.cmd_search()
                self.scene_map.clock_tick()
            elif action in ENV_ACTIONS['take']:
                print self.cmd_take(args)
            elif action in ENV_ACTIONS['drop']:
                print self.cmd_drop(args)
            elif action in ENV_ACTIONS['help']:
                print self.cmd_help()
        else:
            is_valid = False
            print "You can't do that."

        return is_valid

    ##### Command Methods ##### 


    def cmd_look(self):
        """ Execute 'look' command. Print scene descriptions."""
        update_desc(self)
        self.describe()
        self.print_items()
        self.print_clues()

    def cmd_rest(self):
        """ Execute 'rest' command. Return output string."""
        n = ACTION_DURATION['rest']
        player = self.characters['player']
        msg = ["You take a rest ({} hrs).".format(n)]
        # loop until command finished or boss encountered
        for i in xrange(n):
            if self.flags['encounter']:
                msg.append("You are woken up by a noise!")
                player.conditions['surprised'] = True
                break
            msg.append(player.rest())
            self.scene_map.clock_tick()
            if self.scene_map.timeup: # time's up you lose
                break
        # add regular wake up message
        if not self.flags['encounter']:
            msg.append("You wake up from your rest.")
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
                player.conditions['surprised'] = True
                break
            msg.append(player.sleep())
            self.scene_map.clock_tick()
            if self.scene_map.timeup: # time's up you lose
                break
        # add regular wake up message
        if not self.flags['encounter']:
            msg.append("You wake up from your sleep.")
        return '\n'.join(msg)
        
    def cmd_take(self, args):
        """
        Take an item from the scene. Return output string.

        args - itemID as string
        """
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

    def cmd_drop(self, args):
        """
        Drop an item from inventory into the scene. Return output.
        
        args - itemID as string
        """
        player = self.characters['player']
        if not args:
            message = "Please indicate item ID."
        else:
            item = None
            try:
                item = player.inventory[int(args)]
            except:
                return "No such item."
            if item is not None:
                # if item is equipped, unequip it
                if item.equipped:
                    slot = item.desc['slot'][0] # we only need one slot
                    self.cmd_unequip(slot)
                # add item to scene
                self.items.append(item)
                # remove item from inventory
                player.inventory.remove(item)
                message = "Dropped {}.".format(item.desc['name'])
        return message

    def cmd_search(self):
        """ Search the scene. Return output string."""
        uncovered = [] # list of all uncovered items from all item stashes
        lair_msg = None # msg for discovering the lair

        # search all item stashes and lairs in this scene
        for f in self.features:
            if isinstance(f, ItemStash):
                uncovered.extend(f.search())
            if isinstance(f, Lair):
                lair_msg = f.search()
        # add uncovered items to scene.items
        self.items.extend(uncovered)

        msg = ["You spend some time searching."] # start output message
        if uncovered: # not empty
            msg.append("Uncovered the following items:")
            for item in uncovered:
                msg.append(item.desc['name'])
        if lair_msg: # not empty message
            msg.append(lair_msg)
        if not uncovered and not lair_msg: # no discovered items or lairs
            msg.append("You found nothing.")
        return '\n'.join(msg)

    def cmd_help(self):
        """ Return output string containing all commands and shortcuts."""
        message = []
        for cmd, keywords in ENV_ACTIONS.items():
            message.append("{}: {}".format(cmd, keywords))
        return '\n'.join(message)

    def cmd_examine(self, args):
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

    def cmd_unequip(self, args):
        """ Process the 'unequip' command. Return output string."""
        player = self.characters['player']
        # if no arguments specified, return error message
        if not args or args not in player.equipped_names:
            message = "Please indicate slot to unequip. E.g. 'unequip R_hand'"
        else:
            message = player.unequip(args)
        return message

    def cmd_equip(self, args):
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
        """ Print a description of the scene."""
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

    def print_clues(self):
        """ Print description of clues in the scene."""
        if self.clues:
            msg = []
            for clue in self.clues:
                msg.append(clue.get_desc())
            print '\n'.join(msg)

    def get_lair(self):
        """ Return the Lair object from the scene if applicable. Else None."""
        lair = None
        for f in self.features:
            if isinstance(f, Lair):
                lair = f
                break
        return lair

    def update_encounter(self):
        """ Update the scene's encounter flag."""
        lair = self.get_lair()
        if lair:
            if lair.has_boss and lair.revealed:
                self.flags['encounter'] = True
            elif lair.has_boss and not lair.revealed:
                self.flags['encounter'] = False
        else:
            pass

    def print_encounter_msg(self):
        """
        Print a message indicating if the boss is in the area.
        
        Return the printed message (for testing).
        """
        self.update_encounter()
        lair = self.get_lair()
        if self.flags['encounter']: # player sees the boss
            # boss in revealed lair
            if lair and lair.revealed and lair.has_boss: 
                msg = "You can see movement inside the beast's lair!"
                print msg
                return msg
            else: # boss in scene
                msg = "You see the boar! You don't think it notices you."
                print msg
                return msg
        else: # player doesn't see the boss
            return None

    def get_boss_attack(self):
        """ Return True if boss will initiate combat. False otherwise."""
        boar = self.characters['boar']
        # don't attack when bloodied
        if boar.health['HP']/float(boar.effective_stats['max_HP']) < 0.3:
            return False
        # don't attack during daytime
        if self.scene_map.clock.is_day():
            return False
        # otherwise, 50% random chance
        return self.flags['encounter'] and randint(1, 100) <= 50 

    def add_clue(self, clue_class, m_direction):
        """
        Add a clue of the specified type to this scene.
        
        clue_class: Class object to be instantiated
        m_direction: direction of movement returned from move_boss
        """
        # find the clue object of the desired type, if possible
        clue = self.find_clue(clue_class)
        # if there is an existing clue, add to it
        if clue:
            clue.add_clue(direction=m_direction)
        else: # no existing clue, add new clue
            self.clues.append(clue_class(direction=m_direction))
                
    def find_clue(self, clue_class):
        """
        Find the Clue object of the given clue class.

        clue_class: the Class object of the clue
        """
        # return first instance of clue, should also be the only one
        for clue in self.clues:
            if isinstance(clue, clue_class):
                return clue
        return None

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


class TimeUp(Scene):
    """ Special scene for time up (lose). No interaction. Game over."""

    def enter(self):
        print "\n\n"
        print '*' * 30
        print "As the new moon rises, the mad beast bursts out through"
        print "the forest as it makes a beeline for the nearest settlement."
        print "There's no way to catch it now. You've failed."
        print '*' * 20,
        print "GAME OVER",
        print '*' * 20
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

########## SCENE FEATURE CLASS ##########


class Feature(object):
    """
    Base class for a scene feature. Specifies the interface for all subclasses.
    """

    def __init__(self):
        pass

    def get_desc(self):
        """ Return feature description."""
        return "No feature description. Override this method."

########## SCENE FEATURE SUBCLASSES ##########


class Lair(Feature):
    """ A boss lair."""

    def __init__(self):
        """ Initialize lair attributes."""
        self.revealed = False
        self.has_boss = False

    def get_desc(self):
        """ Return lair description if revealed. Otherwise return empty str."""
        if self.revealed:
            return "There's a cave entrance behind the thick brush, it's the \
lair of the forest guardian!"
        else:
            return ""

    def search(self):
        """ Execute a search for the lair."""
        chance = randint(1, 100)
        # 30% chance of discovering the lair in the scene
        if chance <= 30:
            self.revealed = True
            return "You've uncovered a secret lair!"
        else:
            return ""


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
    """ An environmental landmark indicating long-term boss activity."""

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

########## CLUE BASE CLASS ##########


class Clue(object):
    """ A clue indicating recent boss activity."""
    
    def __init__(self, c_type, fresh):
        """
        Initialize clue details. 
        
        c_type: string - clue type
        fresh: freshness, how many ticks is the clue fresh for?
        """
        self.count = 1 # number of clues of this type in the scene, increases
        self.clue_type = c_type
        self.fresh = fresh # >0 is fresh, counts down every tick

    def add_clue(self, direction=None): 
        """ Add one more clue of same type. Extend in subclass."""
        self.count += 1

    def update(self):
        """ Update the clue and desc each clock tick. Extend in subclass."""
        # decrement freshness by 1, lower limit = 0
        self.fresh -= 1
        if self.fresh < 0:
            self.fresh = 0

    def get_desc(self):
        """ Construct and return description string. Override in subclass."""
        return "Please override this method."

########## CLUE SUBCLASSES ##########


class FootprintClue(Clue):
    """ A footprint left by the boss."""

    def __init__(self, direction=None):
        """ Extends Clue.__init__ method."""
        super(FootprintClue, self).__init__("footprint", 2) # fresh for 2 ticks
        self.direction = direction # direction of latest footprints

    def add_clue(self, direction=None): 
        """
        Add one more clue of same type. Extends Clue.add_clue.

        keyword arguments: 
        direction: (string) direction of the newest set of footprints
        """
        super(FootprintClue, self).add_clue()
        self.direction = direction
        self.fresh = 2 # refresh

    def get_desc(self):
        """ Construct and return description string. Overrides Clue.get_desc."""
        msg = []
        full_dir = util.FULL_DIR[self.direction]
        if self.count > 1:
            if self.fresh:
                msg.append(cd.FOOTPRINT['multi_fresh'] % full_dir)
            else:
                msg.append(cd.FOOTPRINT['multi_old'] % full_dir)
        else:
            if self.fresh:
                msg.append(cd.FOOTPRINT['single_fresh'] % full_dir)
            else:
                msg.append(cd.FOOTPRINT['single_old'] % full_dir)
        return ' '.join(msg)


class BrokenTreeClue(Clue):
    """ Trees broken by the boss."""

    def __init__(self, direction=None):
        """ Extends Clue.__init__ method."""
        super(BrokenTreeClue, self).__init__("broken_tree", 2)

    def add_clue(self, direction=None): 
        """
        Add one more clue of same type. Extends Clue.add_clue.
        """
        super(BrokenTreeClue, self).add_clue()
        self.fresh = 2 # refresh

    def get_desc(self):
        """ Construct and return description string. Overrides Clue.get_desc."""
        msg = []
        if self.count > 1:
            if self.fresh:
                msg.append(cd.BROKEN_TREE['multi_fresh'])
            else:
                msg.append(cd.BROKEN_TREE['multi_old'])
        else:
            if self.fresh:
                msg.append(cd.BROKEN_TREE['single_fresh'])
            else:
                msg.append(cd.BROKEN_TREE['single_old'])
        return ' '.join(msg)


class SlainAnimalClue(Clue):
    """ Carcass of slain animals."""

    def __init__(self, direction=None):
        """ Extends Clue.__init__ method."""
        super(SlainAnimalClue, self).__init__("slain_animal", 2)

    def add_clue(self, direction=None): 
        """
        Add one more clue of same type. Extends Clue.add_clue.
        """
        super(SlainAnimalClue, self).add_clue()
        self.fresh = 2 # refresh

    def get_desc(self):
        """ Construct and return description string. Overrides Clue.get_desc."""
        msg = []
        if self.count > 1:
            if self.fresh:
                msg.append(cd.SLAIN_ANIMAL['multi_fresh'])
            else:
                msg.append(cd.SLAIN_ANIMAL['multi_old'])
        else:
            if self.fresh:
                msg.append(cd.SLAIN_ANIMAL['single_fresh'])
            else:
                msg.append(cd.SLAIN_ANIMAL['single_old'])
        return ' '.join(msg)

########## UTILITY FUNCTIONS ##########


def uncover(item, chance):
    """ Return True if a search with the specified chance would
    uncover the item. Otherwise return False."""
    return item.desc['rarity'] <= chance


def update_desc(scene):
    """ Update description of a scene."""
    # Update description of features
    descriptions = []
    for f in scene.features:
        descriptions.append(f.get_desc()) 
    # Update description of exits
    descriptions.append("\nThe path leads towards {}".format(
                                                       scene.exits.keys()))
    scene.description = ' '.join(descriptions)


def get_exit_dir(s1, s2):
    """ Return exit direction from s1 to s2. s1 and s2 are Scene objects."""
    return map_gen.link_direction(s1.location, s2.location)
    
