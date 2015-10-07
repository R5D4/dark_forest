"""
Draw the map with ASCII characters.
"""

import map_gen

SYMBOL_SCENE = '#' # symbol on the map that represents a scene
SYMBOL_PLAYER = 'P' # symbol on the map that represents player's location
SYMBOL_LINK = {
                'n': '|',
                'ne': '/',
                'e': '-',
                'se': '\\',
                's': '|',
                'sw': '/',
                'w': '-',
                'nw': '\\',
                'cross': 'X'
              }


def prepare_canvas(a_map, player_loc):
    """ Create a 2D list representation of the map with ASCII symbols."""
    # create empty canvas (max grid of scenes and links)
    c_size = 2*map_gen.GRID_SIZE - 1
    canvas = [ [ ' ' for i in xrange(c_size) ] for j in xrange(c_size) ]
    # for each scene in the map
    for s1 in a_map.scenes.values():
        # determine the symbol to put on canvas for the scene
        if s1.location  == player_loc: # scene is where the player is
            symbol = SYMBOL_PLAYER
        else:
            symbol = SYMBOL_SCENE
        # determine canvas location of x and y
        x, y = get_canvas_scene_location(s1.location)
        # put a symbol on the canvas for the scene
        canvas[x][y] = symbol
        # for each exit from the scene
        for dir1 in s1.exits.keys():
            # determine canvas location to put the link symbol
            x, y = get_canvas_link_location(s1.location, dir1)
            # choose link symbol
            # if the paths cross, draw an 'x' for crossroad
            if dir1 in ['ne', 'sw'] and canvas[x][y] == '\\' \
                or dir1 in ['nw', 'se'] and canvas[x][y] == '/':
                link_symbol = SYMBOL_LINK['cross']
            else:
                link_symbol = SYMBOL_LINK[dir1]
            # add the link symbol to determined canvas location
            canvas[x][y] = link_symbol
    return canvas


def get_canvas_scene_location(location):
    """ Return corresponding location on the canvas."""
    x, y = location
    # step 1: subtract 1 from x, y since canvas array starts from [0][0]
    x1 = x - 1
    y1 = y - 1
    # step 2: if x or y is greater than 1, add that difference
    x2 = x1 + (x - 1)
    y2 = y1 + (y - 1)
    return (x2, y2)


def get_canvas_link_location(location, direction):
    """ Return link location on canvas given scene's location."""
    # assumption: min location = (1, 1)
    # location + direction does not go off the map

    # get canvas location for the scene
    x, y = get_canvas_scene_location(location)
    # calculate canvas location for the link based on link direction
    dx, dy = map_gen.DIR_TO_DIFF[direction]
    link_loc = (x + dx, y + dy)
    return link_loc


def print_canvas(canvas):
    """ Print out the constructed canvas nicely."""
    c_size = 2*map_gen.GRID_SIZE - 1
    map_string = ""
    for y in xrange(c_size):
        for x in xrange(c_size):
            map_string = "{}{}".format(map_string, canvas[x][y])
        map_string = "{}\n".format(map_string)
    print map_string

