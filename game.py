"""
This is entry point of the game.

Usage:
$ python game.py
"""

import engine
import map_

a_map = map_.Map('story')
a_game = engine.Engine(a_map)
a_game.play()
