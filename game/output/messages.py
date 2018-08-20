from game.output.display_formatter import print_message


def forbidden_field_to_move(direction):
    cardinal_directions = dict(zip(("w", "s", "a", "d"), ("north", "south", "west", "east")))
    message = "You cannot go {}.".format(cardinal_directions[direction])
    print_message(message)
