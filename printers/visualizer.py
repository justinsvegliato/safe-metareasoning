from termcolor import colored

BORDER_CHARACTER = '='
BORDER_STARTER = BORDER_CHARACTER * 5
BORDER_SIZE = 150


def print_planetary_rover_information(planetary_rover_task_process, current_state, policy, grid_world):
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

    height = planetary_rover_task_process.height
    width = planetary_rover_task_process.width

    current_state_record = planetary_rover_task_process.get_state_record_from_state(current_state)

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
            state = planetary_rover_task_process.get_state_from_state_record(state_record)

            factual_state_record = planetary_rover_task_process.get_state_record_from_state(state)

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


def print_safety_process_information(step, execution_contexts, parameter):
    length = len(str(step))

    is_initial_loop = True
    for name in execution_contexts:
        indicator = step if is_initial_loop else " " * length
        print(f"{indicator} {name} State: [{execution_contexts[name]['current_state']}]")
        is_initial_loop = False

    print(f"{' ' * length} \u221F Parameter: [{parameter}]")


def print_header(title):
    print(f"{BORDER_STARTER} {title} ".ljust(BORDER_SIZE, BORDER_CHARACTER))


def print_separator():
    print("=" * BORDER_SIZE)


def print_results(statistics):
    print(f"Cumulative Severity Level 5 Count: {statistics['cumulative_severity_level_count_5']}")
    print(f"Cumulative Severity Level 4 Count: {statistics['cumulative_severity_level_count_4']}")
    print(f"Cumulative Severity Level 3 Count: {statistics['cumulative_severity_level_count_3']}")
    print(f"Cumulative Severity Level 2 Count: {statistics['cumulative_severity_level_count_2']}")
    print(f"Cumulative Severity Level 1 Count: {statistics['cumulative_severity_level_count_1']}")
    print(f"Cumulative Interference: {statistics['cumulative_interference']}")

