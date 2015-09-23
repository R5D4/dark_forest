"""
This is entry point of the game.

Usage:
$ python game.py
"""

import engine
import map_gen
import arena

print "Wecome!"
print "    1. Story"
print "    2. Arena"

while True:
    action = raw_input("Choose a number: ")
    if action == "1":
        a_map = map_gen.new_map()
        a_game = engine.Engine()
        a_game.add_map(a_map)
        a_game.play_story()
    elif action == "2":
        a_arena = arena.Arena()
        a_game = engine.Engine()
        a_game.add_arena(a_arena)
        a_game.play_arena()
    else:
        print "Please enter either '1' or '2'."
