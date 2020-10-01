import math


def print_grid_world_domain(grid_world, current_state):
    height = len(grid_world)
    width = len(grid_world[0])

    current_row = math.floor(current_state / width)
    current_column = current_state - current_row * width

    for row in range(height):
        text = ""

        for column in range(width):
            if row == current_row and column == current_column:
                text += "R"
            elif grid_world[row][column] == 'W':
                text += "\u25A0"
            elif grid_world[row][column] == 'G':
                text += "\u272A"
            elif grid_world[row][column] == 'S':
                text += "\u229B"
            else:
                text += "\u25A1"
            text += "  "

        print(f"{text}")


def print_grid_world_policy(grid_world, policy):
    symbols = {
        'STAY': '\u2205',
        'NORTH': '\u2191',
        'EAST': '\u2192',
        'SOUTH': '\u2193',
        'WEST': '\u2190'
    }

    for row in range(len(grid_world)):
        text = ""

        for column in range(len(grid_world[row])):
            state = len(grid_world[row]) * row + column
            if grid_world[row][column] == 'W':
                text += "\u25A0"
            else:
                text += symbols[policy[state]]
            text += "  "

        print(f"{text}")