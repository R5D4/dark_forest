from sys import exit
from random import randint
import char
import combat

class Scene(object):

    def process_action(self, action):
        print "Please override this method."

    def describe(): 
        print "Please override this method."
    
    def print_encounter_msg(self):
        if self.flags['encounter']:
            print "You see the boar! You don't think it notices you."

    # determine encounter chance
    # chance - encounter chance (0,1)
    def encounter(self, chance):
        return randint(1,10) <= (chance * 10)

    # default enter method for interactive scenes
    def enter(self):
        self.describe()
        chance = self.flags['encounter_chance']
        self.flags['encounter'] = self.encounter(chance)
        self.print_encounter_msg()
        
        while True:
            action = raw_input("> ")
            # trying to leave
            if action in self.exits.keys() and self.flags['can_leave']:
                return self.exits.get(action) 
            elif combat.ATTACK in action and self.flags['encounter']:
                return combat.begin_combat(self.characters)
            else: 
                self.process_action(action)


class Death(Scene):

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
        self.describe()
        return 'start_area'


class StartArea(Scene):

    """Area 1"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'ne': 'dead_log_area',
            'se': 'ponds_area'
        }
        self.flags = {
            'can_leave': True,
            'on_tree': False,
            'can_dodge': True,
            'encounter': False,
            'encounter_chance': 0.1
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

    """Area 2"""

    def __init__(self, characters):
        self.characters = characters
        self.exits = {
            'sw': 'start_area',
            'e': 'dead_end',
            'se': 'brook_area'
        }
        self.flags = {
            'can_leave': True,
            'encounter_chance': 0.2
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


class Map(object):

    """ Defines the map, maps scene name to objects """

    def __init__(self, start_scene_name):
        self.roll_characters()
        self.scenes = {
            'story': Story(),
            'death': Death(),
            'win': Win(),
            'quit': Quit(),
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
        self.start_scene_name = start_scene_name

    # Returns a Scene object for the next scene.
    def next_scene(self, scene_name):
        return self.scenes.get(scene_name)

    # Returns a Scene object for the opening scene.
    def opening_scene(self):
        return self.next_scene(self.start_scene_name)

    # Roll characters
    def roll_characters(self):
        response = 'y'
        while response == 'y':
            self.characters = {}
            print "\nRolling player character:"
            print "-" * 20
            self.characters['player'] = char.Player(0)
            response = raw_input("Reroll character? (y/n): ")

        response = 'y'
        while response == 'y':
            print "\nRolling boss character:"
            print "-" * 20
            self.characters['boar'] = char.Boar(0)
            response = raw_input("Reroll character? (y/n): ")
            
