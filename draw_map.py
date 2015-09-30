"""
Draw the map with ASCII characters.
"""

def draw_test():
    """ Quick test to see how the map would look."""
    bitmap = [
                [' ', ' ', '#'],
                [' ', ' ', '|'],
                [' ', ' ', '#'],
                [' ', '/', ' '],
                ['#', ' ', ' ']
             ]

    map_string = ""
    for row in bitmap:
        for col in row:
            map_string = "{}{}".format(map_string, col)
        map_string = "{}\n".format(map_string)
    print map_string
