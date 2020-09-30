import math

from termcolor import colored

BORDER_SIZE = 150


def print_states(mdp):
    print("States:")

    for index, state in enumerate(mdp.states()):
        print(f"  State {index}: {state}")


def print_actions(mdp):
    print("Actions:")

    for index, action in enumerate(mdp.actions()):
        print(f"  Action {index}: {action}")


def print_transition_function(mdp):
    print("Transition Function:")

    is_valid = True

    for state in mdp.states():
        for action in mdp.actions():
            print(f"  Transition: ({state}, {action})")

            total_probability = 0

            for successor_state in mdp.states():
                probability = mdp.transition_function(state, action, successor_state)

                total_probability += probability

                if probability > 0:
                    print(f"    Successor State: {successor_state} -> {probability}")

            is_valid = is_valid and 0.99 <= total_probability <= 1.01
            print(f"    Total Probability: {total_probability}")

            if not is_valid:
                return

    print(f"  Is Valid: {is_valid}")


def print_reward_function(mdp):
    print("Reward Function:")

    for state in mdp.states():
        print(f"  State: {state}")

        for action in mdp.actions():
            reward = mdp.reward_function(state, action)
            print(f"    Action: {action} -> {reward}")


def print_start_state_function(mdp):
    print("Start State Function:")

    total_probability = 0

    for state in mdp.states():
        probability = mdp.start_state_function(state)

        if probability > 0:
            print(f"  State {state}: {probability}")
        
        total_probability += probability

    print(f"  Total Probability: {total_probability}")

    is_valid = 0.99 <= total_probability <= 1.01
    print(f"  Is Valid: {is_valid}")


def print_mdp(mdp):
    print_states(mdp)
    print_actions(mdp)
    print_transition_function(mdp)
    print_reward_function(mdp)
    print_start_state_function(mdp)


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


def print_mars_rover_policy(mars_rover_mdp, current_state, policy, grid_world):
    symbols = {
        'NORTH': '\u2191',
        'EAST': '\u2192',
        'SOUTH': '\u2193',
        'WEST': '\u2190',
        'REBOOT': '\u21BA',
        'TRANSMIT': '\u21AF',
        'CHARGE': '\u263C',
        'ANALYZE': '\u25CE',
        'NOMINAL': '\u2713',
        'ERROR': '\u2717',
        'ANALYZED': '\u2713',
        'NOT_ANALYZED': '\u2717',
    }

    height = mars_rover_mdp.height
    width = mars_rover_mdp.width

    current_state_record = mars_rover_mdp.get_state_record_from_state(current_state).copy()

    print("===== System Metrics ".ljust(BORDER_SIZE, '='))

    remaining_battery = "#" * current_state_record['battery_level']
    depleted_battery = "-" * (5 - current_state_record['battery_level'])
    print(f"|{remaining_battery}{depleted_battery}| \u00B7 {current_state_record['battery_level']}")

    print(f"{symbols[current_state_record['water_analyzer_health']]} Water Analyzer")
    print(f"{symbols[current_state_record['soil_analyzer_health']]} Soil Analyzer")

    for point_of_interest, analysis_status in current_state_record['analysis_status'].items():
        print(f"{symbols[analysis_status]} {point_of_interest}")

    print("===== Control Policy ".ljust(BORDER_SIZE, '='))

    for row in range(height):
        text = ""

        for column in range(width):
            state_record = current_state_record.copy()
            state_record['row'] = row
            state_record['column'] = column
            state = mars_rover_mdp.get_state_from_state_record(state_record)

            factual_state_record = mars_rover_mdp.get_state_record_from_state(state)

            symbol = None

            if grid_world[row][column] == 'W':
                symbol = "\u25A0"
            else:
                symbol = symbols[policy[state]]

            if state_record == current_state_record:
                symbol = colored(symbol, 'red')
            elif factual_state_record['weather'] == 'SHADY':
                symbol = colored(symbol, 'blue', attrs=['dark'])

            text += symbol
            text += "  "

        print(f"{text}")


def print_mlc_information(step, mlc_execution_contexts, parameter):
    length = len(str(step))

    is_initial_loop = True
    for name in mlc_execution_contexts:
        indicator = step if is_initial_loop else " " * length
        print(f"{indicator} {name} State: [{mlc_execution_contexts[name]['current_state']}]")
        is_initial_loop = False

    print(f"{' ' * length} \u221F Parameter: [{parameter}]")
