"""
This is entry point of the game.

Usage:
$ python game.py
"""

import engine
import map_

print "Wecome!"
print "    1. Story"
print "    2. Arena"

while True:
    action = raw_input("Choose a number: ")
    if action == "1":
        a_map = map_.Map('story')
        a_game = engine.Engine(a_map)
        a_game.play()
    elif action == "2":
        a_game = engine.Engine(None)
        a_game.arena()
    else:
        print "Please enter either '1' or '2'."
