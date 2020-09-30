import math

from termcolor import colored

BORDER_CHARACTER = '='
BORDER_STARTER = BORDER_CHARACTER * 5
BORDER_SIZE = 150


def print_mars_rover_visualization(mars_rover_olp, current_state, policy, grid_world):
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

    height = mars_rover_olp.height
    width = mars_rover_olp.width

    current_state_record = mars_rover_olp.get_state_record_from_state(current_state)

    print_header("System Metrics")

    remaining_battery = "#" * current_state_record['battery_level']
    depleted_battery = "-" * (5 - current_state_record['battery_level'])
    print(f"|{remaining_battery}{depleted_battery}| \u00B7 {current_state_record['battery_level']}")

    print(f"{symbols[current_state_record['water_analyzer_health']]} Water Analyzer")
    print(f"{symbols[current_state_record['soil_analyzer_health']]} Soil Analyzer")

    for point_of_interest, analysis_status in current_state_record['analysis_status'].items():
        print(f"{symbols[analysis_status]} {point_of_interest}")

    print_header("Control Policy")

    for row in range(height):
        text = ""

        for column in range(width):
            state_record = current_state_record.copy()
            state_record['row'] = row
            state_record['column'] = column
            state = mars_rover_olp.get_state_from_state_record(state_record)

            factual_state_record = mars_rover_olp.get_state_record_from_state(state)

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


def print_mlc_information(step, execution_contexts, parameter):
    length = len(str(step))

    is_initial_loop = True
    for name in execution_contexts:
        is_initial_loop = False

        indicator = step if is_initial_loop else " " * length
        print(f"{indicator} {name} State: [{execution_contexts[name]['current_state']}]")

    print(f"{' ' * length} \u221F Parameter: [{parameter}]")


def print_header(title):
    print(f"{BORDER_STARTER} {title} ".ljust(BORDER_SIZE, BORDER_CHARACTER))


def print_separator():
    print("=" * BORDER_SIZE)
